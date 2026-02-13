
const chatBox = document.getElementById("chatBox");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

// send from composer
if (sendBtn) {
  sendBtn.addEventListener("click", () => {
    const text = input.value.trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";
    sendToServer(text);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendBtn.click();
  });
}

// quick buttons
document.querySelectorAll(".quick-buttons button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const msg = btn.dataset.msg;
    addMessage(btn.textContent, "user");
    sendToServer(msg);
  });
});

// Message function with clickable links
function addMessage(text, who = "bot") {
  const wrapper = document.createElement("div");

  if (who === "user") {
    wrapper.className = "user-msg";
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;
    wrapper.appendChild(bubble);
  } else if (who === "bot") {
    wrapper.className = "bot-msg";
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    wrapper.appendChild(bubble);
  } else if (who === "typing") {
    wrapper.className = "bot-msg typing";
    wrapper.innerHTML =
      "<span class='dot'></span><span class='dot'></span><span class='dot'></span>";
  }

  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
  return wrapper;
}

function removeTyping(node) {
  if (node) node.remove();
}

//  Typing effect function
function typeText(element, text, speed = 20) {
  const linkedText = text.replace(
    /(https?:\/\/[^\s]+)/g,
    '<a href="$1" target="_blank" class="chat-link">$1</a>'
  );
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = linkedText;
  const fullText = tempDiv.innerHTML;

  let i = 0;
  const typingInterval = setInterval(() => {
    element.innerHTML = fullText.slice(0, i);
    i++;
    chatBox.scrollTop = chatBox.scrollHeight;
    if (i > fullText.length) clearInterval(typingInterval);
  }, speed);
}

async function sendToServer(message) {
  const typingNode = addMessage("", "typing");
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });
    const data = await res.json();
    removeTyping(typingNode);

    // create bot bubble
    const botMsg = addMessage("", "bot");
    const bubble = botMsg.querySelector(".bubble");

    typeText(bubble, data.reply, 10);
  } catch (e) {
    removeTyping(typingNode);
    addMessage("⚠️ Error connecting to server.", "bot");
    console.error(e);
  }
}
