// Drag and Drop functionality
const dragDropBox = document.getElementById('drag-drop-box');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results');
const scanDetails = document.getElementById('scan-details');
const chatbotSection = document.getElementById('chatbot-section');
let uploaded = false;

// Handle file upload
uploadBtn.addEventListener('click', () => {
  const files = fileInput.files;
  if (files.length > 0) {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }

    fetch('/upload', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        uploaded = true;  // Mark that a file has been uploaded
        alert(data.message);  // Notify user

        // Show the chatbot section after uploading
        chatbotSection.style.display = 'block';
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
});

// Chatbot functionality
const sendBtn = document.getElementById('sendBtn');
sendBtn.addEventListener('click', () => {
  const userText = document.getElementById('userInput').value;
  if (userText.trim() !== '') {
    appendChat('You', userText);
    getChatbotResponse(userText);
    document.getElementById('userInput').value = ''; // Clear input after sending
  }
});

// Send user input to the Flask server
function getChatbotResponse(userText) {
  if (!uploaded) {
    appendChat('AI', 'Please upload a file first.');
    return; // Don't proceed if no file has been uploaded
  }

  fetch('/chatbot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ userText: userText }), // Send the user text
  })
    .then(response => response.json())
    .then(data => {
      // Append the response from the server to the chat
      appendChat('AI', data.response);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Append message to chat log
function appendChat(sender, text) {
  const chatLog = document.getElementById('chat-log');
  const message = document.createElement('p');
  message.textContent = `${sender}: ${text}`;
  chatLog.appendChild(message);
  chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
}
