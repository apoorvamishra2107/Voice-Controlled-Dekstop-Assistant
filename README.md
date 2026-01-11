# Voice-Controlled Desktop Assistant

A Python-based voice assistant that can perform a wide range of desktop operations, including opening apps, websites, files, searching YouTube, creating folders, taking screenshots, typing, scrolling, and more — all via voice commands.

---

## Features

- **Open any installed application** on your system (e.g., WhatsApp Business, Spotify, Chrome).  
- **Open websites** dynamically (e.g., YouTube, Google, LinkedIn, WhatsApp Web).  
- **Search YouTube** directly by voice command (e.g., "Search BTS song on YouTube").  
- **Create folders** in Documents via voice.  
- **Open any file** by specifying its path.  
- **Desktop automation**: typing, scrolling, taking screenshots.  
- **Close apps** using voice commands.  
- **Exit** the assistant via voice command.

---

## Prerequisites

1. **Python 3.10+** (tested with Python 3.13)  
2. **Microphone** for voice input  
3. **System access** for file and app operations  

### Python Dependencies

Install required Python packages:

```bash
pip install pyttsx3 pyautogui sounddevice soundfile numpy glob2
pip install git+https://github.com/openai/whisper.git
