document.addEventListener('DOMContentLoaded', () => {
    const redactBtn = document.getElementById('redact-btn');
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');

    redactBtn.addEventListener('click', () => {
        const text = inputText.value;

        fetch('http://localhost:5000/redact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.redacted_text) {
                outputText.textContent = data.redacted_text;
            } else if (data.error) {
                outputText.textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            outputText.textContent = 'An error occurred while communicating with the backend.';
        });
    });
});
