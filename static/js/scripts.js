// scripts.js

document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const message = document.getElementById('message').value;
    console.log('Message submitted:', message);
    document.getElementById('message').value = '';
});
