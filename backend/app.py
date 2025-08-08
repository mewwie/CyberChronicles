# backend/app.py
from flask import Flask, request, jsonify
from redactor import redact_pii

app = Flask(__name__)

@app.route('/redact', methods=['POST'])
def handle_redact():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, "text" field is required.'}), 400

    text = data['text']
    redacted_text = redact_pii(text)

    return jsonify({'redacted_text': redacted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
