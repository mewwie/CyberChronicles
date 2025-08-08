import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2

# Aangenomen dat redactor.py bestaat met een redact_text functie
from redactor import redact_text

# --- Dependency Configuration ---
# Voor meer geavanceerde PII-redactie kan een bibliotheek als spaCy worden gebruikt.
# Het model zou hier worden geladen.
# Voorbeeld:
# import spacy
# nlp = spacy.load("en_core_web_sm")
# -----------------------------

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# Maak mappen aan als ze niet bestaan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Controleert of het bestandstype is toegestaan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    """Extraheert tekst uit een PDF-bestand."""
    text = ""
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        # Hier zou je logging toevoegen
        print(f"Error extracting PDF text: {e}")
        raise
    return text

@app.route('/redact', methods=['POST'])
def handle_redact():
    """Verwerkt redactieverzoeken voor tekst en bestanden."""
    options = {
        'mode': request.form.get('mode', 'replace'),
        'mask_char': request.form.get('mask_char', 'X'),
    }

    # Handle text input
    if 'text' in request.form and request.form.get('text'):
        text = request.form.get('text')
        redacted_text = redact_text(text, options=options)
        return jsonify({'redacted': redacted_text})

    # Handle file input
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed.'}), 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        try:
            if filename.lower().endswith('.txt'):
                with open(upload_path, 'r', encoding='utf-8') as f:
                    original_text = f.read()
            elif filename.lower().endswith('.pdf'):
                original_text = extract_text_from_pdf(upload_path)
            else:
                # Should be unreachable due to allowed_file check
                return jsonify({'error': 'Internal error: unexpected file type.'}), 500

            redacted_text = redact_text(original_text, options=options)

            redacted_filename = f"redacted_{os.path.splitext(filename)[0]}.txt"
            download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], redacted_filename)
            with open(download_path, 'w', encoding='utf-8') as f:
                f.write(redacted_text)

            download_link = f"/download/{redacted_filename}"
            return jsonify({
                'redacted_result': 'File processed successfully.',
                'download_link': download_link
            })
        except Exception as e:
            print(f"Error processing file: {e}")
            return jsonify({'error': 'An internal error occurred while processing the file.'}), 500
        finally:
            if os.path.exists(upload_path):
                os.remove(upload_path)

    return jsonify({'error': 'No text or file input provided.'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    """Stelt een geredigeerd bestand beschikbaar om te downloaden."""
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
