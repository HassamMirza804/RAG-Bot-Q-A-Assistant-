document.addEventListener('DOMContentLoaded', function() {
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');
    const uploadSection = document.getElementById('upload-section');
    const chatSection = document.getElementById('chat-section');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    // const spinner = document.getElementById('spinner'); // Removed

    // Handle session start with the dummy PDF
    uploadBtn.addEventListener('click', () => {
        uploadStatus.textContent = 'Processing...';
        uploadStatus.style.color = 'white';
        uploadBtn.disabled = true;

        // Simulate a small delay for a more realistic feel
        setTimeout(() => {
            uploadStatus.textContent = 'Session started!';
            uploadStatus.style.color = 'green';
            
            // Hide upload section and show chat section
            uploadSection.style.display = 'none';
            chatSection.style.display = 'flex';

            // NEW: Auto-scroll the chat box to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 1500); // Wait for 1.5 seconds
    });

    // Handle chat messages
    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        const userBubble = document.createElement('div');
        userBubble.classList.add('message-bubble', 'user-message');
        userBubble.textContent = message;
        chatBox.appendChild(userBubble);
        userInput.value = '';
        
        // NEW: Auto-scroll the chat box to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // spinner.style.display = 'block'; // Removed
        // sendBtn.disabled = true; // Kept but spinner line removed

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: message }),
            });

            const data = await response.json();
            const botMessage = data.answer;

            const botBubble = document.createElement('div');
            botBubble.classList.add('message-bubble', 'bot-message');
            botBubble.textContent = botMessage;
            chatBox.appendChild(botBubble);
            
            // NEW: Auto-scroll the chat box to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;

        } catch (error) {
            const errorBubble = document.createElement('div');
            errorBubble.classList.add('message-bubble', 'bot-message');
            errorBubble.textContent = 'Sorry, an error occurred.';
            chatBox.appendChild(errorBubble);
        } finally {
            // spinner.style.display = 'none'; // Removed
            sendBtn.disabled = false;
            userInput.focus();
        }
    };

    // Listen for button click
    sendBtn.addEventListener('click', sendMessage);

    // Listen for Enter key press
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});