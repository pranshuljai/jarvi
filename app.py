from flask import Flask, request, jsonify
import os
import platform
import webbrowser
import pyttsx3
import wikipediaapi
import yt_dlp

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate

# Initialize Wikipedia API with a user agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='JarvisAI/1.0 (https://github.com/your_username/jarvis-ai)'  # Specify your user agent here
)

# Register Chrome as the browser
chrome_path = r'C:/Users/pc/AppData/Local/Google/Chrome/Application/chrome.exe'  # Update this path if necessary
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def wikipedia_search(search_term):
    """Fetch summary from Wikipedia based on the search term."""
    page = wiki_wiki.page(search_term)
    if page.exists():
        summary = page.summary[:500]  # Get the first 500 characters of the summary
        return summary
    else:
        return f"Sorry, I couldn't find any information on {search_term}."

def open_website(website_name):
    """Open websites dynamically based on the website name."""
    url = f"https://www.{website_name}.com"
    webbrowser.get('chrome').open(url)

def open_image(search_term):
    """Open an image search based on the search term."""
    webbrowser.get('chrome').open(f"https://www.google.com/search?hl=en&tbm=isch&q={search_term.replace(' ', '+')}")

def play_song(song_name):
    """Play a song based on the song name using YouTube."""
    search_query = '+'.join(song_name.split())
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'extract_flat': True,  # Only search, don't download
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{search_query}", download=False)
        if info_dict and 'entries' in info_dict and len(info_dict['entries']) > 0:
            video_url = info_dict['entries'][0]['url']
            webbrowser.get('chrome').open(video_url)
        else:
            return "Sorry, I couldn't find that song."

@app.route('/command', methods=['POST'])
def command():
    command = request.get_json()['command']
    if "what is" in command or "tell me about" in command or "world war" in command:
        search_term = command.replace("what is", "").replace("tell me about", "").strip()
        result = wikipedia_search(search_term)
        return jsonify({'response': result})
    elif "open" in command:
        website_name = command.replace("open", "").strip()
        open_website(website_name)
        return jsonify({'response': f"Got it, sir. Opening {website_name}."})
    elif "open images of" in command:
        search_term = command.replace("open images of", "").strip()
        open_image(search_term)
        return jsonify({'response': f"Got it, sir. Opening images for {search_term}."})
    elif "play" in command:
        song_name = command.replace("play", "").strip()
        result = play_song(song_name)
        if result:
            return jsonify({'response': result})
        else:
            return jsonify({'response': f"Got it, sir. Playing {song_name}."})
    else:
        return jsonify({'response': "Sorry, I didn't understand that command."})

if __name__ == '__main__':
    app.run(debug=True)