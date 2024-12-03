// script.js

// 1. Dropdown menu for "Recent Chats"
const recentChatsHeader = document.querySelector('.recent-chats h3');
const recentChatsList = document.querySelector('.recent-chats ul');

recentChatsHeader.addEventListener('click', () => {
  recentChatsList.classList.toggle('show');
});

// 2. Functionality for the search bar
const searchInput = document.querySelector('.search');

searchInput.addEventListener('input', () => {
  // Filter recent chats based on search input
  const searchTerm = searchInput.value.toLowerCase();
  const chatItems = recentChatsList.querySelectorAll('li');

  chatItems.forEach(item => {
    const chatText = item.textContent.toLowerCase();
    if (chatText.includes(searchTerm)) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  });
});

// 3. Send button action (e.g., sending the prompt to an API)
const sendButton = document.querySelector('.send-button');
const promptInput = document.querySelector('.prompt-input');

sendButton.addEventListener('click', () => {
  const prompt = promptInput.value;

  // Here you would typically make an API call to send the prompt
  // to your AI model. Replace the following with your actual API call.
  console.log('Sending prompt to API:', prompt);

  // Optionally clear the input field
  promptInput.value = '';
});

// 4. Voice input functionality
const voiceInput = document.querySelector('.voice-input');

voiceInput.addEventListener('click', () => {
  // Here you would integrate a speech recognition API (e.g., Web Speech API)
  // to capture user's voice input and convert it to text.
  console.log('Voice input activated');

  // Example using Web Speech API (ensure browser compatibility)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    promptInput.value = transcript;
    console.log('Transcript:', transcript);
  };

  recognition.start();
});