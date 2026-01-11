import whisper
import sounddevice as sd
import numpy as np
import pyttsx3
import pyautogui
import subprocess
import webbrowser
import os
import time
import glob

# ----------------------------
# Text to Speech
# ----------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ----------------------------
# Load Whisper Model
# ----------------------------
print("Loading Whisper model...")
model = whisper.load_model("base")  # "small" for better accuracy
print("Whisper loaded")

# ----------------------------
# Record Audio
# ----------------------------
def record_audio(duration=5, fs=16000):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="float32")
    sd.wait()
    return np.squeeze(audio)

# ----------------------------
# Listen Function
# ----------------------------
def listen():
    try:
        audio = record_audio()
        result = model.transcribe(audio, language="en")
        command = result["text"].strip().lower()
        print("Command:", command)
        return command
    except Exception as e:
        print("Error:", e)
        return ""

# ----------------------------
# Open any installed app dynamically
# ----------------------------
def open_app(app_name):
    app_name = app_name.lower()
    paths = [
        os.environ.get("ProgramFiles", "C:\\Program Files"),
        os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", "") + "\\Programs"
    ]
    
    exe_name = app_name.replace(" ", "") + ".exe"
    found = None

    for path in paths:
        if not path:
            continue
        for file in glob.glob(f"{path}/**/{exe_name}", recursive=True):
            found = file
            break
        if found:
            break

    if found:
        try:
            subprocess.Popen(found)
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Could not open {app_name}")
    else:
        speak(f"Could not find {app_name} installed on your system")

# ----------------------------
# Open websites intelligently
# ----------------------------
def open_website(site_name):
    site_name = site_name.lower()
    websites = {
        "linkedin": "https://www.linkedin.com",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com"
    }
    url = websites.get(site_name, f"https://www.{site_name.replace(' ', '')}.com")
    speak(f"Opening {site_name}")
    webbrowser.open(url)

# ----------------------------
# Search on YouTube
# ----------------------------
def search_youtube(query):
    query = query.replace("search ", "").replace("on youtube", "").strip()
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    speak(f"Searching YouTube for {query}")
    webbrowser.open(url)

# ----------------------------
# Create folder in Documents
# ----------------------------
def create_folder(folder_name):
    folder_path = os.path.join(os.path.expanduser("~\\Documents"), folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        speak(f"Folder {folder_name} created in Documents")
    except Exception as e:
        speak("Could not create folder")

# ----------------------------
# Command Execution
# ----------------------------
def execute_command(command):
    if not command:
        return

    # Exit commands
    if any(x in command for x in ["exit", "stop assistant", "quit"]):
        speak("Goodbye")
        exit()

    # Search on YouTube
    if "search" in command and "youtube" in command:
        search_youtube(command)
        return

    # Create new folder
    if "create folder" in command:
        folder_name = command.replace("create folder", "").strip()
        create_folder(folder_name)
        return

    # Open files
    if command.startswith("open file "):
        path = command.replace("open file ", "").strip()
        if os.path.exists(path):
            os.startfile(path)
            speak(f"Opening file {os.path.basename(path)}")
        else:
            speak("File not found")
        return

    # Open apps or websites
    if command.startswith("open "):
        site_or_app = command.replace("open ", "").strip()
        if any(keyword in site_or_app for keyword in [".com", "www", "linkedin", "youtube", "google", "whatsapp", "facebook", "twitter"]):
            open_website(site_or_app)
        else:
            open_app(site_or_app)
        return

    # Screenshots
    if "screenshot" in command or "take screenshot" in command:
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/screenshot_{int(time.time())}.png"
        pyautogui.screenshot(filename)
        speak("Screenshot taken")
        return

    # Typing text
    if command.startswith("type "):
        text = command.replace("type ", "")
        pyautogui.write(text, interval=0.05)
        speak("Typed successfully")
        return

    # Scrolling
    if "scroll down" in command:
        pyautogui.scroll(-500)
        return
    if "scroll up" in command:
        pyautogui.scroll(500)
        return

    # Closing apps
    if command.startswith("close "):
        app_name = command.replace("close ", "").strip()
        try:
            subprocess.call(f"taskkill /im {app_name}.exe /f", shell=True)
            speak(f"Closed {app_name}")
        except Exception as e:
            speak(f"Could not close {app_name}")
        return

    # Fallback
    speak("Sorry, I don't know how to do that yet.")

# ----------------------------
# Main Loop
# ----------------------------
speak("Voice assistant started. Say exit to stop.")

while True:
    cmd = listen()
    execute_command(cmd)
