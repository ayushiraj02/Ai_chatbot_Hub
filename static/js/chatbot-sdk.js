// chatbot-sdk.js
// This script handles the chatbot functionality, including sending messages, toggling delete mode, and managing bot selection.
document.addEventListener('DOMContentLoaded', function () {

  // Delete Mode toggle
  const deleteToggle = document.getElementById('toggleDeleteMode');
  if (deleteToggle) {
    deleteToggle.addEventListener('click', () => {
      const checkboxes = document.querySelectorAll('.selectCheckbox');
      const selectHeader = document.getElementById('selectHeader');
      const deleteWrapper = document.getElementById('deleteSelectedWrapper');
      const isHidden = checkboxes[0].style.display === 'none';

      checkboxes.forEach(cb => cb.style.display = isHidden ? 'table-cell' : 'none');
      selectHeader.style.display = isHidden ? 'table-cell' : 'none';
      deleteWrapper.style.display = isHidden ? 'block' : 'none';
    });
  }

  // Select All functionality
  const selectAll = document.getElementById('selectAll');
  if (selectAll) {
    selectAll.addEventListener('change', function () {
      const checkboxes = document.querySelectorAll('input[name="bot_ids"]');
      checkboxes.forEach(cb => cb.checked = this.checked);
    });
  }

  // Send chat message
  const sendBtn = document.getElementById('sendMessage');
  if (sendBtn) {
    sendBtn.addEventListener('click', () => {
      const input = document.getElementById('userInput');
      const apiKey = document.getElementById('botSelector').value;
      const message = input.value.trim();

      if (!message) {
        alert('Please enter a message.');
        return;
      }

      const chatBox = document.getElementById('chatMessages');
      chatBox.innerHTML += `<div class="text-end mb-2"><strong>You:</strong> ${message}</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;

      fetch('/bots/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: message, api_key: apiKey })
      })
      .then(response => response.json())
      .then(data => {
        let reply = data.response ? data.response : data.error ? `Error: ${data.error}` : 'Unexpected response';
        chatBox.innerHTML += `<div class="text-start mb-2"><strong>Bot:</strong> ${reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch(error => {
        console.error('Chat error:', error);
        chatBox.innerHTML += `<div class="text-danger text-start mb-2">Error sending message.</div>`;
      });

      input.value = '';
    });
  }

  // Bot switch loader
  const botSelector = document.getElementById('botSelector');
  if (botSelector) {
    botSelector.addEventListener('change', () => {
      const loader = document.getElementById('botLoader');
      loader.style.display = 'block';
      setTimeout(() => loader.style.display = 'none', 1000);
    });
  }

});
