const inputField = document.getElementById('inputField');
const submitButton = document.getElementById('submitButton');
const responseContainer = document.getElementById('responseContainer');

submitButton.addEventListener('click', () => {
  const input = inputField.value;

  // Create request payload
  const payload = {
    input: input
  };

  // Make POST request to localhost:3000
  fetch('http://localhost:3000', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.text())
  .then(data => {
    // Update UI with response
    responseContainer.textContent = data;
  })
  .catch(error => {
    console.error('Error:', error);
    responseContainer.textContent = 'Error occurred during API request';
  });
});
