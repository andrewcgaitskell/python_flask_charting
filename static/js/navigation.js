 function togglePanel() {
        var panel = document.getElementById("sidePanel");
        var mainContent = document.getElementById("main-content");

        if (panel.style.left === "-250px") {
            panel.style.left = "0";
            mainContent.style.marginLeft = "250px";
        } else {
            panel.style.left = "-250px";
            mainContent.style.marginLeft = "0";
        }
    }

// JavaScript function to go back to the previous page
function goBack() {
    window.history.back();
}
