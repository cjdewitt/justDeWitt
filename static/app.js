document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatbox = document.getElementById('chatbox');
    const messageInput = document.getElementById('message');

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message === '') return;

        // Display user's message with animation
        appendMessage('You', message, 'user-message', true);

        // Clear input
        messageInput.value = '';

        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'message': message })
        })
        .then(response => response.json())
        .then(data => {
            // Display bot's reply with animation
            appendMessage('assistant', data.reply, 'bot-message', true);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Error', 'There was an error processing your request.', 'bot-message', true);
        });
    });

    function appendMessage(sender, message, className, animate = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        if (animate) {
            messageElement.style.opacity = '0';
            messageElement.style.transform = 'translateY(20px)';
        }
        messageElement.innerHTML = `<strong>${sender}</strong> ${message}`;
        chatbox.appendChild(messageElement);
        
        // Clear float and force new line between message groups
        const clearDiv = document.createElement('div');
        clearDiv.style.clear = 'both';
        chatbox.appendChild(clearDiv);

        // Animate the message appearance
        if (animate) {
            setTimeout(() => {
                messageElement.style.transition = 'all 0.3s ease';
                messageElement.style.opacity = '1';
                messageElement.style.transform = 'translateY(0)';
            }, 100);
        }

        chatbox.scrollTop = chatbox.scrollHeight;
    }
});