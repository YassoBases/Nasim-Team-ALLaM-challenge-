document.addEventListener('DOMContentLoaded', function () {
    const toggleSwitch = document.getElementById('theme-toggle');
    const body = document.body;

    // Load the saved theme from local storage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.className = savedTheme;
        toggleSwitch.checked = savedTheme === 'dark-mode';
    }

    // Toggle theme between light and dark mode
    toggleSwitch.addEventListener('change', function () {
        if (toggleSwitch.checked) {
            body.className = 'dark-mode';
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.className = 'light-mode';
            localStorage.setItem('theme', 'light-mode');
        }
    });
});

// Function to clear the chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat?')) {
        // Here you'd handle the actual logic for clearing chat
        alert('Chat cleared.');
    }
}

// Function to clear the history
function clearHistory() {
    if (confirm('Are you sure you want to clear the history?')) {
        // Here you'd handle the actual logic for clearing history
        alert('History cleared.');
    }
}
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('change', function() {
    if (this.checked) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
    }
});
// Existing theme toggling code (if any)

// Add this below:
document.querySelectorAll('input, select').forEach((element) => {
    element.addEventListener('focus', (e) => {
        e.target.style.backgroundColor = "#f0f0f0"; // Gray highlight on focus
    });
    element.addEventListener('blur', (e) => {
        e.target.style.backgroundColor = "#f8f8f8"; // Return to default
    });
});
