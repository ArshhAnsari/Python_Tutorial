import time  # for adding delays
import speech_recognition as sr  # speech-to-text via Google API
import webbrowser  # to open web pages
import win32com.client as wincl  # Windows COM interface for text-to-speech

# ——— Setup —————————————————————————————————————————————————————
# Create a Recognizer instance to capture and interpret audio input
recognizer = sr.Recognizer()

# Initialize the Windows SAPI text-to-speech engine
speaker = wincl.Dispatch("SAPI.SpVoice")
# Set the speaker volume (0 to 100)
speaker.Volume = 100
# Set the speaking rate (-10 to +10; 0 is default)
speaker.Rate = 0


def speak(text: str):
    """
    Convert text to speech using Windows SAPI and pause briefly.

    :param text: The string to verbalize
    :return: None (blocks until speech is finished)
    """
    # Log the phrase for debugging
    print(f"[speak] → {text!r}")
    # Speak the phrase
    speaker.Speak(text)
    # Small delay to allow audio device to free up before listening again
    time.sleep(0.3)


# ——— Ambient Noise Calibration —————————————————————————————————————
# Capture 1 second of ambient audio to set a noise threshold
# This improves speech recognition accuracy in noisy environments
with sr.Microphone() as src:
    recognizer.adjust_for_ambient_noise(src, duration=1)
    print("Calibrated for ambient noise.")


# ——— Command Processing ——————————————————————————————————————————

def process_command(cmd: str):
    """
    Interpret a spoken command string and perform the corresponding action.

    Supported commands:
    - "open youtube": opens YouTube in the default browser
    - "open google": opens Google
    - "open facebook": opens Facebook
    - "open twitter": opens X (formerly Twitter)
    - "open github": opens GitHub
    - "open stackoverflow": opens Stack Overflow
    - "open chat gpt": opens ChatGPT website
    - otherwise: informs the user the command was not understood

    :param cmd: Raw command string (case-insensitive)
    :return: None
    """
    cmd = cmd.lower()  # normalize to lowercase for easier matching

    if "open youtube" in cmd:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open google" in cmd:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in cmd:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open twitter" in cmd:
        speak("Opening Twitter")
        webbrowser.open("https://x.com")  # X is the new Twitter domain
    elif "open github" in cmd:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
    elif "open stackoverflow" in cmd:
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif "open chat gpt" in cmd:
        speak("Opening Chat G P T")
        webbrowser.open("https://chatgpt.com")
    else:
        # No matching command found
        speak("Sorry, I didn't understand that command.")


# ——— Listening Functions ———————————————————————————————————————————

def listen_for_wake_word() -> bool:
    """
    Listen for a short phrase and check if the wake word "jarvis" is spoken.

    Uses a small time limit to avoid long blocking listens.

    :return: True if "jarvis" detected, False otherwise
    """
    with sr.Microphone() as src:
        print("Listening for wake word...")
        audio = recognizer.listen(src, phrase_time_limit=4, timeout=3)

    try:
        # Convert audio to text via Google Speech Recognition
        phrase = recognizer.recognize_google(audio)
        print("Heard wake word:", phrase)
        return "jarvis" in phrase.lower()
    except sr.UnknownValueError:
        # Could not understand audio
        return False
    except sr.RequestError as e:
        # API was unreachable or unresponsive
        print("Recognition error:", e)
        return False


def listen_for_command() -> str:
    """
    Listen indefinitely for a user command after wake word is detected.

    :return: The recognized command string
    :raises: sr.UnknownValueError if speech is unintelligible
             sr.RequestError if the API is unreachable
    """
    with sr.Microphone() as src:
        print("Listening for your command...")
        audio = recognizer.listen(src)

    # Return the raw recognized text (case as spoken)
    result = recognizer.recognize_google(audio)
    print("Heard command raw:", result)
    return result


# ——— Main Execution Loop ————————————————————————————————————————————

if __name__ == "__main__":
    # Announce startup
    speak("Initializing Jarvis")

    # Continuously listen for wake word and commands
    while True:
        try:
            # If wake word detected, prompt and process a command
            if listen_for_wake_word():
                speak("Yes, Sir?")
                cmd = listen_for_command()
                print("Command:", cmd)
                process_command(cmd)

        except sr.UnknownValueError:
            # Fallback if speech was unclear
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            # Handle API connectivity issues
            speak("Speech service is down.")
            print(e)
        except KeyboardInterrupt:
            # Allow graceful shutdown on Ctrl+C
            speak("Shutting down. Goodbye!")
            break
        except Exception as e:
            # Catch-all for any unexpected errors
            print("Unexpected error:", e)
            break
