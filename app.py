from modules.activity_loader import load_activity
from modules.voice_engine import speak, listen_command
from modules.activity_manager import ActivityManager

# Lazy import for camera
camera_imported = False
start_camera = None

def run():
    global camera_imported, start_camera

    # Load activity
    activity = load_activity("led_activity.json")
    name = activity["activity_name"]
    description = activity["description"]
    components = activity["components"]
    steps = activity["steps"]

    manager = ActivityManager(steps)

    print(f"\n=== Activity: {name} ===\n")

    # Speak intro
    speak(f"Activity name is {name}")
    speak(description)

    speak("Components required are:")
    for comp in components:
        speak(comp)

    speak("Say start to begin the activity. Say help for available commands.")

    # MAIN LOOP
    while True:
        # Listen and normalize command
        command = listen_command()
        if command:
            command = command.lower().strip()
        else:
            command = ""

        if command == "":
            speak("Command not recognized. Please repeat.")
            continue  # retry

        # START
        if "start" in command:
            step = manager.start()
            speak("Starting activity")
            speak(step)

        # NEXT STEP
        elif "next" in command:
            if not manager.started:
                speak("Please say start first")
            else:
                step = manager.next_step()
                speak(step)

        # PREVIOUS STEP
        elif "previous" in command or "back" in command:
            if not manager.started:
                speak("Please say start first")
            else:
                step = manager.previous_step()
                speak(step)

        # REPEAT STEP
        elif "repeat" in command or "again" in command:
            if not manager.started:
                speak("Please say start first")
            else:
                step = manager.repeat_step()
                speak(step)

        # CAMERA DETECTION
        elif "camera" in command:
            if not camera_imported:
                from modules.camera_module import start_camera as sc
                start_camera = sc
                camera_imported = True
            speak("Opening camera for detection")
            start_camera()

        # HELP
        elif "help" in command:
            speak("Available commands are: start, next, previous, repeat, camera, exit, help")

        # EXIT
        elif "exit" in command or "quit" in command:
            speak("Exiting program")
            break

        # INVALID
        else:
            speak("Invalid command. Say help to list all commands")


if __name__ == "__main__":
    run()