from flask import Flask, jsonify, request, render_template
import speech_recognition as sr
import threading

app = Flask(__name__)


recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Bufor do przechowywania rozpoznanego tekstu
recognized_text = []

def record_audio():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Kalibracja poziomu szumu
        while True:
            print("Nagrywanie...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                recognized_text.append(text)
                print(f"Rozpoznano: {text}")
            except sr.UnknownValueError:
                print("Nie udało się rozpoznać mowy.")
            except sr.RequestError:
                print("Błąd usługi Google API.")

@app.route('/start', methods=['POST'])
def start_recording():
    thread = threading.Thread(target=record_audio)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "recording_started"}), 200

@app.route('/stop', methods=['POST'])
def stop_recording():
    # Funkcja stop nie jest zaimplementowana w ten sposób - są to przykładowe założenia
    # Zazwyczaj kontroluje się to na poziomie klienta lub przez specjalne zarządzanie wątkami.
    return jsonify({"status": "recording_stopped", "data": recognized_text}), 200

@app.route('/')
def index():
    return render_template('index.html')


from flask_socketio import SocketIO, emit
import speech_recognition as sr

socketio = SocketIO(app)

def recognize_stream():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(m, callback)

def callback2(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        print("Rozpoznano: {}".format(text))
        socketio.emit('new_text', {'text': text})
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def callback(recognizer, audio):
    try:
        # Tymczasowo użyj domyślnego języka jako języka do rozpoznawania
        # Zaprojektuj to, aby uzyskać odpowiedni język z frontendu za pomocą SocketIO
        global language  # Przechowaj aktualnie wybrany język globalnie

        text = recognizer.recognize_google(audio, language=language)
        print(language + ": " + format(text) )
        socketio.emit('new_text', {'text': text})
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


@socketio.on('set_language')
def handle_language_change(json):
    global language  # Przechowaj aktualnie wybrany język globalnie
    language = json['language']
    print('Language changed to: ' + language)


if __name__ == '__main__':
    global language  # Przechowaj aktualnie wybrany język globalnie
    language = 'en-US'  # Przykład domyślnego języka

    recognize_stream()
    socketio.run(app, debug=True)


#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)