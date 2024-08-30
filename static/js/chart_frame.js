// chart_frame.js

// Send screen dimensions to Flask endpoint when the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Get the screen width and height
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Send the dimensions to the Flask server using Fetch API
    fetch('/get_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ width: screenWidth, height: screenHeight })
    })
});
