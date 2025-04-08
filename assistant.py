import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import random
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text: str) -> None:
    """Speak the given text."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    """Listen to the user's voice command and return it as text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        command_text = sr.Recognizer().recognize_google(audio_data)
        print(f"You said: {command_text}")
        return command_text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, the speech service is not available.")
        return ""

def greet_user() -> None:
    """Greet the user based on the current time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning shreedevi!")
    elif hour < 18:
        speak("Good afternoon shreedevi!")
    else:
        speak("Good evening shreedevi!")
    speak("How can I help you today?")

def play_local_music() -> None:
    """Play a random music file from the user's music folder."""
    music_folder = "C:\\Users\\user\\Music"  # Adjust if needed
    if os.path.exists(music_folder):
        songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        if songs:
            song = random.choice(songs)
            song_path = os.path.join(music_folder, song)
            speak(f"Playing {song}")
            os.startfile(song_path)
        else:
            speak("No music files found.")
    else:
        speak("Music folder not found.")

def tell_joke() -> None:
    """Tell a random joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything.",
        "What did one wall say to the other? I'll meet you at the corner.",
        "Why did the computer go to therapy? It had too many bytes!"
    ]
    speak(random.choice(jokes))

def execute_command(command_text: str) -> None:
    """Execute the given voice command."""
    if "time" in command_text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")

    elif "search for" in command_text:
        query = command_text.replace("search for", "").strip()
        speak(f"Searching for {query}")
        pywhatkit.search(query)

    elif "play" in command_text and "youtube" in command_text:
        song = command_text.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "play music" in command_text:
        play_local_music()

    elif "wikipedia" in command_text:
        topic = command_text.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(topic, sentences=1)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError:
            speak("That topic is too broad. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("That topic could not be found on Wikipedia.")

    elif "open google" in command_text:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command_text:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "tell me a joke" in command_text:
        tell_joke()

    elif "how are you" in command_text:
        speak("I'm doing great, thank you! How about you?")

    elif "exit" in command_text or "goodbye" in command_text:
        speak("Goodbye Anjali! Have a nice day.")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")

# Run the assistant
if __name__ == "__main__":
    greet_user()
    while True:
        user_command = listen()
        if user_command:
            execute_command(user_command)
