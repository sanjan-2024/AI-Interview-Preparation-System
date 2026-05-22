document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('chat-toggle');
  const widget = document.getElementById('chat-widget');
  const closeBtn = document.getElementById('chat-close');
  const sendBtn = document.getElementById('chat-send');
  const input = document.getElementById('chat-input-widget');
  const windowEl = document.getElementById('chat-window-widget');
  const avatar = document.getElementById('chat-avatar-img');

  function openWidget() {
    widget.classList.add('open');
    // focus input when opened
    setTimeout(() => input.focus(), 200);
    // small dance when opened
    triggerAnimate();
  }
  function closeWidget() {
    widget.classList.remove('open');
  }

  toggle.addEventListener('click', function (e) {
    e.preventDefault();
    openWidget();
  });
  closeBtn.addEventListener('click', closeWidget);

  function appendMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = 'chat-message ' + (role === 'bot' ? 'bot-message' : 'user-message');
    msg.innerHTML = `<div class="message-text">${text}</div>`;
    windowEl.appendChild(msg);
    windowEl.scrollTop = windowEl.scrollHeight;
  }

  function triggerAnimate() {
    if (!avatar) return;
    avatar.classList.remove('blink');
    avatar.classList.remove('dance');
    // force reflow
    void avatar.offsetWidth;
    avatar.classList.add('blink');
    avatar.classList.add('dance');
  }

  async function sendMessage(text) {
    appendMessage('user', text);
    appendMessage('bot', '...');
    triggerAnimate();
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      // replace last bot '...' message
      const bots = windowEl.querySelectorAll('.bot-message');
      if (bots.length) {
        bots[bots.length - 1].querySelector('.message-text').innerText = data.reply;
      } else {
        appendMessage('bot', data.reply);
      }
      triggerAnimate();
    } catch (err) {
      const bots = windowEl.querySelectorAll('.bot-message');
      if (bots.length) bots[bots.length - 1].querySelector('.message-text').innerText = 'Sorry, something went wrong.';
    }
  }

  // send on button
  sendBtn.addEventListener('click', function () {
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    sendMessage(text);
  });
  // send on enter
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendBtn.click();
    }
  });
});