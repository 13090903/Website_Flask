function getText() {
    var message = document.getElementById("text-input").value;
    var messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
}
