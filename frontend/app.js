document.addEventListener('DOMContentLoaded', () => {
    const textForm = document.getElementById('text-form');
    const fileForm = document.getElementById('file-form');
    const resultDiv = document.getElementById('result-div');

    textForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(textForm);

        fetch('http://localhost:5000/redact', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.redacted) {
                resultDiv.innerHTML = `<pre>${data.redacted}</pre>`;
            } else if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p>An error occurred while communicating with the backend.</p>';
        });
    });

    fileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(fileForm);

        fetch('http://localhost:5000/redact', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.download_link) {
                resultDiv.innerHTML = `<p>${data.redacted_result} <a href="http://localhost:5000${data.download_link}" target="_blank">Download Redacted File</a></p>`;
            } else if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p>An error occurred while communicating with the backend.</p>';
        });
    });
});
