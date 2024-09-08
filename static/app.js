async function sendCommand() {
    const command = document.getElementById('command').value;
    const response = await fetch('/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command })
    });
    const result = await response.json();
    document.getElementById('output').innerText = result.response;
}

function startListening() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript;
            document.getElementById('command').value = command;
            sendCommand();
        };
        recognition.start();
    } else {
        alert('Speech recognition not supported in this browser.');
    }
}

