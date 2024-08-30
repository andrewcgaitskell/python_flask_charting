// css_variable.js

document.addEventListener('DOMContentLoaded', function () {
    // Get the value of the CSS variable
    const root = document.documentElement;
    const mainColor = getComputedStyle(root).getPropertyValue('--main-color').trim();

    // Update the fetch URL to match the Blueprint prefix
    fetch('/charts/receive_css_variable', {  // Use the correct URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mainColor: mainColor })  // Send the CSS variable value as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error sending CSS variable:', error);
    });
});
