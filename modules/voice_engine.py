import pyttsx3
import speech_recognition as sr

def speak(text):
    """
    Convert text to speech
    """
    print(f"[AI]: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen_command(timeout=7, phrase_time_limit=5):
    """
    Listen for a voice command and return normalized command string.
    Maps similar words to expected commands.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("[AI]: Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command_raw = recognizer.recognize_google(audio)
            command_raw = command_raw.lower()
            print(f"[User]: {command_raw}")

            # Map similar phrases to commands
            if any(x in command_raw for x in ["start", "begin"]):
                return "start"
            elif any(x in command_raw for x in ["next", "step forward", "go ahead"]):
                return "next"
            elif any(x in command_raw for x in ["previous", "back", "go back"]):
                return "previous"
            elif any(x in command_raw for x in ["repeat", "say again", "repeat step"]):
                return "repeat"
            elif any(x in command_raw for x in ["camera", "photo", "detect"]):
                return "camera"
            elif any(x in command_raw for x in ["help", "commands", "what can i say"]):
                return "help"
            elif any(x in command_raw for x in ["exit", "quit", "stop"]):
                return "exit"
            else:
                return ""  # not recognized

        except sr.WaitTimeoutError:
            print("[AI]: No speech detected.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Please repeat.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is not available.")
            return ""