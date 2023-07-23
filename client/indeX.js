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
  .then(response => {
    // Check if the response is successful
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // Parse the response as text
    return response.text();
  })
  .then(data => {
    // Create a Blob from the response data
    const blob = new Blob([data], { type: 'text/csv' });

    // Create a URL for the Blob
    const url = window.URL.createObjectURL(blob);

    // Get the download link element and update its attributes
    const downloadLink = document.getElementById('downloadLink');
    downloadLink.href = url;
    downloadLink.download = 'data.csv';

    // Simulate a click on the download link to trigger the download
    downloadLink.click();

    // Hide the download link
    downloadLink.style.display = 'none';

    // Update UI with a success message
    responseContainer.textContent = 'File download initiated. Check your browser\'s download bar.';
  })
  .catch(error => {
    console.error('Error:', error);
    responseContainer.textContent = 'Error occurred during API request';
  });
});

