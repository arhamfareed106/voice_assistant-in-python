from flask import Flask, request, jsonify, render_template
import pyttsx3
import wikipedia
import time
import os
import pywhatkit as pw
import webbrowser as wb

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)


app = Flask(__name__)

voice = pyttsx3.init()
voice.setProperty('rate', 150)

responses = {
    "who is your developer": "Ahmad Khawaja is my developer",
    "who is your inventor": "Ahmad Khawaja is my developer",
    "who is your father": "Ahmad Khawaja is my developer"
}

def handle_command(command):
    command = command.lower()
    response = ""

    if command in responses:
        response = responses[command]

    elif "clear chat" in command:
        os.system("cls" if os.name == "nt" else "clear")
        response = "Chat cleared"

    elif "exit" in command:
        response = "Thanks for using me. Goodbye!"
        voice.say(response)
        voice.runAndWait()
        exit()

    elif "on google" in command:
        search_query = command.replace("on google", "").strip()
        pw.search(search_query)
        response = f"Searching Google for {search_query}"

    elif "open" in command:
        website = command.replace("open ", "").strip()
        url = f"https://{website}.com"
        wb.open(url)
        response = f"Opening {url}"

    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        response = f"The current time is {current_time}"

    elif "play" in command:
        video_query = command.replace("play", "").strip()
        pw.playonyt(video_query)
        response = f"Playing {video_query} on YouTube"

    elif "whatsapp" in command:
        response = "WhatsApp functionality is not implemented in this example."

    elif "weather" in command:
        response = "Weather functionality is not implemented in this example."

    else:
        try:
            result = wikipedia.summary(command, sentences=3)
            response = result
        except wikipedia.exceptions.DisambiguationError as e:
            response = f"Multiple results found: {', '.join(e.options)}"
        except wikipedia.exceptions.PageError:
            response = "No results found"

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data.get('command', '')
    response = handle_command(command)
    voice.say(response)
    voice.runAndWait()
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change the port if necessary
