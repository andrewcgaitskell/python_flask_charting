// script.js

document.addEventListener('DOMContentLoaded', function () {
    // Get the value of the CSS variable
    const root = document.documentElement;
    const screenWidth = getComputedStyle(root).getPropertyValue('----screen-width').trim();

    // Optional: Send the value to the Flask server
    fetch('/charts/receive_css_variable', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ screenWidth: screenWidth })  // Send the CSS variable value as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error sending CSS variable:', error);
    });
});
