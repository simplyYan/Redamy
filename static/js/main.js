document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButton = document.getElementById('theme-toggle');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatOutput = document.getElementById('chat-output');
    
    // Load theme from local storage
    const currentTheme = localStorage.getItem('theme') || 'light';
    setTheme(currentTheme);
    themeToggleButton.addEventListener('click', function () {
        const newTheme = document.body.classList.contains('light-mode') ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });

    function setTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
            document.getElementById('theme-toggle').textContent = "💡 Light Theme";
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
            document.getElementById('theme-toggle').textContent = "🌒 Dark Theme";
        }
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('User', message);
        userInput.value = '';

        // Enviar mensagem ao backend e obter resposta
        $.get("/get", { msg: message }).done(function(data) {
            appendMessage('Redamy', data);
        });
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('my-2', 'p-2', 'rounded');
        messageElement.style.backgroundColor = sender === 'User' ? '#d1ecf1' : '#c3e6cb';
        messageElement.textContent = `${sender}: ${message}`;
        chatOutput.appendChild(messageElement);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }
});
