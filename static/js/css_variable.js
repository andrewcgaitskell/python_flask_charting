// css_variable.js

 // Function to update CSS variables with actual screen size
function updateScreenSizeVars() {
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Update CSS variables
    document.documentElement.style.setProperty('--screen-width', `${screenWidth}px`);
    document.documentElement.style.setProperty('--screen-height', `${screenHeight}px`);

    // Update content on the page
    document.getElementById('width').textContent = screenWidth;
    document.getElementById('height').textContent = screenHeight;
}

// Initial update on page load
updateScreenSizeVars();

// Update on window resize
window.addEventListener('resize', updateScreenSizeVars);

document.addEventListener('DOMContentLoaded', function () {
    // Get the value of the CSS variable
    const root = document.documentElement;
    const mainColor = getComputedStyle(root).getPropertyValue('--main-color').trim();
    const screenHeight = getComputedStyle(root).getPropertyValue('--screen-width').trim();
    const screenWidth = getComputedStyle(root).getPropertyValue('-screen-height').trim();

    // Update the fetch URL to match the Blueprint prefix
    fetch('/charts/receive_css_variable', {  // Use the correct URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mainColor: mainColor, screenHeight: screenHeight, screenWidth : screenWidth })  // Send the CSS variable value as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error sending CSS variable:', error);
    });
});
