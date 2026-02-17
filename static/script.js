const chatBox = document.getElementById("chat-box");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    addMessage("Thinking...", "bot");

    fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.lastChild.innerText = data.advice;
    })
    .catch(() => {
        chatBox.lastChild.innerText = "Error getting response.";
    });
}

