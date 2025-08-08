import os
import uuid
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pii_redactor import redact_pii
from pypdf import PdfReader
import docx

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey' # Needed for flashing messages

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_text_from_file(filepath):
    """
    Extracts text from a file.
    """
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()
    text = ""
    if extension == '.txt':
        with open(filepath, 'r') as f:
            text = f.read()
    elif extension == '.pdf':
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text()
    elif extension == '.docx':
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + '\n'
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redact', methods=['POST'])
def redact():
    chat_id = uuid.uuid4()
    original_input = None
    input_filename = None
    has_error = False

    if 'text' in request.form and request.form['text']:
        original_input = request.form['text']
        redacted_text, has_error = redact_pii(original_input, chat_id)
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            original_input = get_text_from_file(filepath)
            input_filename = filename # Keep track for saving on error
            redacted_text, has_error = redact_pii(original_input, chat_id)

            # Clean up the uploaded file if there are no errors
            if not has_error:
                os.remove(filepath)
        else:
            flash('Invalid file type')
            return redirect(request.url)
    else:
        flash('No input provided')
        return redirect(url_for('index'))

    if has_error:
        if 'text' in request.form and request.form['text']:
            # Save the text input to a file
            error_filename = f"{chat_id}_error.txt"
            with open(os.path.join(app.config['UPLOAD_FOLDER'], error_filename), 'w') as f:
                f.write(original_input)
            flash('An error occurred during redaction. The original text has been saved.')
        elif input_filename:
             # The file is already saved, just flash a message
            flash('An error occurred during redaction. The original file has been saved.')

    return render_template('redacted.html', redacted_text=redacted_text)

# We need a template to display the result
@app.route('/redacted')
def redacted():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
