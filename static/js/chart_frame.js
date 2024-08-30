// chart_frame.js

// Send screen dimensions to Flask endpoint when the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Get the screen width and height
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Send the dimensions to the Flask server using Fetch API
    fetch('/get_dimensions', {
        method: 'GET',
        headers: {
            'Content-Type': 'text/plain'
        },
        body: { width: screenWidth, height: screenHeight }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Assume the server responds with JSON
    });
});
