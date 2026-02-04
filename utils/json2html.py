import json
import streamlit as st
import os
import hashlib
from gtts import gTTS
import tempfile

import json
import streamlit as st
import os
import hashlib
from gtts import gTTS
import tempfile
import base64
from io import BytesIO

def generate_audio_base64(text, lang='en'):
    """Generate audio data as base64 string from text using gTTS"""
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to BytesIO buffer
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode()
        return f"data:audio/mpeg;base64,{audio_base64}"
        
    except Exception as e:
        print(f"Error generating audio for '{text}': {e}")
        return None
welcome_text = "Welcome to the Daily Vocabulary Service. Enjoy learning new words every day!"
welcome_voice = generate_audio_base64(welcome_text)
# st.markdown(f'<audio controls><source src="{welcome_voice}" type="audio/mpeg"></audio>', unsafe_allow_html=True)

def generate_combined_audio_file(word, meaning, phrase, lang='en'):
    """Generate combined audio file with word, meaning, and phrase"""
    try:
        # Create audio directory if it doesn't exist
        audio_dir = "audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        
        # Create filename based on the word
        filename = f"{word.replace(' ', '_').lower()}.mp3"
        file_path = os.path.join(audio_dir, filename)
        
        # Generate combined text with pauses
        combined_text = f"{word}. . . {meaning}. . . {phrase}"
        
        # Generate audio file if it doesn't exist
        if not os.path.exists(file_path):
            tts = gTTS(text=combined_text, lang=lang, slow=False)
            tts.save(file_path)
        
        return filename
        
    except Exception as e:
        print(f"Error generating combined audio file: {e}")
        return None

def get_combined_audio_base64(word, meaning, phrase, lang='en'):
    """Get combined audio as base64 data"""
    try:
        # Create combined text with pauses
        combined_text = f"{word}. . . {meaning}. . . {phrase}"
        
        # Generate base64 audio
        tts = gTTS(text=combined_text, lang=lang, slow=False)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Convert to base64
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode()
        return f"data:audio/mpeg;base64,{audio_base64}"
        
    except Exception as e:
        print(f"Error generating combined audio: {e}")
        return None

def json_to_vocabulary_html(word_data):
    """Convert vocabulary JSON data to HTML with audio playback"""
    
    if not isinstance(word_data, dict):
        return ""
    
    # Extract vocabulary components
    word = word_data.get('word', '')
    meaning = word_data.get('meaning', '')
    phrase = word_data.get('phrase', '')
    
    # Generate combined audio file and save to audio folder
    audio_filename = generate_combined_audio_file(word, meaning, phrase)
    
    # Also get base64 version for embedding
    combined_audio_base64 = get_combined_audio_base64(word, meaning, phrase)
    
    # Generate individual base64 audio data for individual buttons
    word_audio = generate_audio_base64(word)
    meaning_audio = generate_audio_base64(meaning)
    phrase_audio = generate_audio_base64(phrase)
    
    # Create unique IDs for audio elements
    combined_id = f"combined_audio_{hashlib.md5(word.encode()).hexdigest()[:8]}"
    word_id = f"word_audio_{hashlib.md5(word.encode()).hexdigest()[:8]}"
    meaning_id = f"meaning_audio_{hashlib.md5(meaning.encode()).hexdigest()[:8]}"
    phrase_id = f"phrase_audio_{hashlib.md5(phrase.encode()).hexdigest()[:8]}"
    
    # Build HTML with audio elements - using inline styles for portability
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }}
            p {{
                font-size: 18px;
                margin: 10px 0;
                line-height: 1.6;
            }}
            .audio-controls {{
                margin: 20px 0;
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }}
            .play-button {{
                background-color: #4CAF50;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }}
            .play-button:hover {{
                background-color: #45a049;
            }}
            .play-button:disabled {{
                background-color: #cccccc;
                cursor: not-allowed;
            }}
            .play-button.playing {{
                background-color: #ff9800;
            }}
            .status {{
                margin-top: 15px;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
                min-height: 25px;
                font-style: italic;
                color: #666;
            }}
            .audio-element {{
                display: none;
            }}
        </style>
    </head>
    <body>
        <p><strong>word:</strong> {word}</p>
        <p><strong>meaning:</strong> {meaning}</p>
        <p><strong>phrase:</strong> {phrase}</p>
        
        <div class="audio-controls">
            <button class="play-button" onclick="playSequentially()">🔊 Play All</button>
            <button class="play-button" onclick="playAudio('{word_id}', this)">Play Word</button>
            <button class="play-button" onclick="playAudio('{meaning_id}', this)">Play Meaning</button>
            <button class="play-button" onclick="playAudio('{phrase_id}', this)">Play Phrase</button>
        </div>
        
        <div class="status" id="status"></div>
        
        <!-- Hidden audio elements -->"""
    
    # Add combined audio element
    if combined_audio_base64:
        html_content += f'\n        <audio id="{combined_id}" class="audio-element" preload="auto"><source src="{combined_audio_base64}" type="audio/mpeg"></audio>'
    
    # Add individual audio elements with base64 data if generated successfully
    if word_audio:
        html_content += f'\n        <audio id="{word_id}" class="audio-element" preload="auto"><source src="{word_audio}" type="audio/mpeg"></audio>'
    if meaning_audio:
        html_content += f'\n        <audio id="{meaning_id}" class="audio-element" preload="auto"><source src="{meaning_audio}" type="audio/mpeg"></audio>'
    if phrase_audio:
        html_content += f'\n        <audio id="{phrase_id}" class="audio-element" preload="auto"><source src="{phrase_audio}" type="audio/mpeg"></audio>'
    
    html_content += f"""
        
        <script>
            function updateStatus(message) {{
                const status = document.getElementById('status');
                if (status) {{
                    status.textContent = message;
                    setTimeout(() => {{
                        status.textContent = '';
                    }}, 2000);
                }}
            }}
            
            function playAudio(audioId, button) {{
                const audio = document.getElementById(audioId);
                if (audio) {{
                    // Reset all buttons
                    document.querySelectorAll('.play-button').forEach(btn => {{
                        btn.classList.remove('playing');
                        btn.disabled = false;
                    }});
                    
                    // Mark current button as playing
                    button.classList.add('playing');
                    button.disabled = true;
                    
                    audio.currentTime = 0;
                    
                    audio.onended = function() {{
                        button.classList.remove('playing');
                        button.disabled = false;
                        updateStatus('Finished playing');
                    }};
                    
                    audio.onerror = function() {{
                        button.classList.remove('playing');
                        button.disabled = false;
                        updateStatus('Error playing audio');
                    }};
                    
                    const playPromise = audio.play();
                    if (playPromise !== undefined) {{
                        playPromise.then(() => {{
                            updateStatus('Playing audio...');
                        }}).catch((error) => {{
                            console.error('Error playing audio:', error);
                            button.classList.remove('playing');
                            button.disabled = false;
                            updateStatus('Failed to play audio');
                        }});
                    }}
                }} else {{
                    updateStatus('Audio not available');
                }}
            }}
            
            function playSequentially() {{
                // First try to play the combined audio
                const combinedAudio = document.getElementById('{combined_id}');
                if (combinedAudio) {{
                    combinedAudio.currentTime = 0;
                    const playPromise = combinedAudio.play();
                    if (playPromise !== undefined) {{
                        playPromise.then(() => {{
                            updateStatus('Playing complete vocabulary...');
                        }}).catch((error) => {{
                            console.error('Error playing combined audio:', error);
                            // Fallback to individual audio playback
                            playIndividualSequence();
                        }});
                    }}
                    
                    combinedAudio.onended = function() {{
                        updateStatus('Finished playing complete vocabulary');
                    }};
                    
                    combinedAudio.onerror = function() {{
                        // Fallback to individual audio playback
                        playIndividualSequence();
                    }};
                }} else {{
                    // Fallback to individual audio playback
                    playIndividualSequence();
                }}
            }}
            
            function playIndividualSequence() {{
                const audioIds = ['{word_id}', '{meaning_id}', '{phrase_id}'];
                const labels = ['word', 'meaning', 'phrase'];
                let currentIndex = 0;
                
                // Disable all buttons during sequential play
                document.querySelectorAll('.play-button').forEach(btn => {{
                    btn.disabled = true;
                }});
                
                function playNext() {{
                    if (currentIndex < audioIds.length) {{
                        const audio = document.getElementById(audioIds[currentIndex]);
                        const label = labels[currentIndex];
                        
                        if (audio) {{
                            updateStatus(`Playing ${{label}}...`);
                            audio.currentTime = 0;
                            
                            audio.onended = function() {{
                                setTimeout(() => {{
                                    currentIndex++;
                                    playNext();
                                }}, 800); // 800ms pause between audio
                            }};
                            
                            audio.onerror = function() {{
                                currentIndex++;
                                playNext();
                            }};
                            
                            const playPromise = audio.play();
                            if (playPromise !== undefined) {{
                                playPromise.catch((error) => {{
                                    console.error('Error playing audio:', error);
                                    currentIndex++;
                                    playNext();
                                }});
                            }}
                        }} else {{
                            currentIndex++;
                            playNext();
                        }}
                    }} else {{
                        // Re-enable all buttons
                        document.querySelectorAll('.play-button').forEach(btn => {{
                            btn.disabled = false;
                        }});
                        updateStatus('Finished playing all');
                    }}
                }}
                
                updateStatus('Starting individual playback...');
                playNext();
            }}
            
            // Auto-play combined audio on load
            window.onload = function() {{
                const audioSupported = !!(document.createElement('audio').canPlayType);
                if (!audioSupported) {{
                    updateStatus('Audio not supported in this browser');
                }} else {{
                    updateStatus('Loading audio...');
                    // Auto-play with immediate attempt
                    setTimeout(() => {{
                        playSequentially();
                    }}, 500);
                }}
            }};
        </script>
    </body>
    </html>
    """
    
    return html_content

def json_to_simple_html(data):
    """Convert JSON data to simple HTML content"""
    
    def convert_value(key, value):
        if isinstance(value, dict):
            html = f"<h3>{key}</h3>\n"
            for k, v in value.items():
                html += convert_value(k, v)
            return html
            
        elif isinstance(value, list):
            html = f"<h3>{key}</h3>\n<ul>\n"
            for item in value:
                if isinstance(item, dict):
                    html += "<li>\n"
                    for k, v in item.items():
                        html += f"<strong>{k}:</strong> {v}<br>\n"
                    html += "</li>\n"
                else:
                    html += f"<li>{item}</li>\n"
            html += "</ul>\n"
            return html
            
        else:
            return f"<p><strong>{key}:</strong> {value}</p>\n"
    
    # Build simple HTML
    html_body = ""
    if isinstance(data, dict):
        for key, value in data.items():
            html_body += convert_value(key, value)
    
    # Create simple HTML
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h3 {{ color: #333; }}
            p {{ margin: 5px 0; }}
            ul {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    return html_content

# Sample vocabulary data
word = {
    "word": "serendipity",
    "meaning": "the occurrence and development of events by chance in a happy or beneficial way",
    "phrase": "Finding this book was pure serendipity"
}

"""
# Generate vocabulary HTML with audio
vocabulary_html = json_to_vocabulary_html(word)

# Display HTML inside Streamlit
st.components.v1.html(vocabulary_html, height=500, scrolling=True)

simple_html = json_to_simple_html(word)
st.components.v1.html(simple_html, height=300, scrolling=True)

"""