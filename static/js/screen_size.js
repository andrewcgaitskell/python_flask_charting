// base.js
// screen_size.js

document.addEventListener('DOMContentLoaded', function () {
    // Function to update CSS variables with actual screen size and send them to the server
    function updateScreenSizeVarsAndSendData() {
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;

        // Update CSS variables
        document.documentElement.style.setProperty('--screen-width', `${screenWidth}px`);
        document.documentElement.style.setProperty('--screen-height', `${screenHeight}px`);

        // Update content on the page
        const widthElement = document.getElementById('width');
        const heightElement = document.getElementById('height');

        if (widthElement) widthElement.textContent = screenWidth;
        if (heightElement) heightElement.textContent = screenHeight;

        // Get the value of the CSS variable
        const root = document.documentElement;

        // Read updated CSS variable values
        const mainColor = getComputedStyle(root).getPropertyValue('--main-color').trim();
        const updatedScreenHeight = getComputedStyle(root).getPropertyValue('--screen-height').trim();
        const updatedScreenWidth = getComputedStyle(root).getPropertyValue('--screen-width').trim();

        // Update the fetch URL to match the Blueprint prefix
        fetch('/charts/receive_css_variable', {  // Use the correct URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mainColor: mainColor,
                screenHeight: updatedScreenHeight,
                screenWidth: updatedScreenWidth
            })  // Send the CSS variable value as JSON
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error sending CSS variable:', error);
        });
    }

    // Initial update on page load
    updateScreenSizeVarsAndSendData();

    // Update on window resize and send data
    window.addEventListener('resize', updateScreenSizeVarsAndSendData);
});
