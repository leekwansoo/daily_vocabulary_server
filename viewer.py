"""
viewer.py

Display vocabulary words with audio playback.

Usage examples:
  # Standalone mode (no Streamlit required)
  python viewer.py

  # Streamlit mode
  streamlit run viewer.py

  # Import and use in other scripts
  from viewer import view_trigger_standalone
  view_trigger_standalone()
"""
import asyncio
import os
import json
import time
import webbrowser
import tempfile
from datetime import timedelta
from datetime import datetime, timezone
from utils.select_words import select_words_from_vocabulary
from utils.json2html import json_to_vocabulary_html # (word_data) return html_content

# Try to import streamlit, but make it optional
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False



# Get the env variables for SMTP server configuration



def get_today_iso_date():
    # Use local date for comparison (strip time)
    return datetime.now().date().isoformat()


def build_html_from_vocabulary(words):
    # Build plain text and simple HTML
    lines = []
    html_lines = ["<html><body>", "<h2>Today's Mailed Words</h2>", "<ul>"]

    for w in words:
        print("Processing word for email content:", w)
        word = w.get('word', '')
        meaning = w.get('meaning', '')
        phrase = w.get('phrase', '')
        media = w.get('media', '')
        
        
        lines.append(f"- {word} | {meaning} | {phrase} | {media}")
        html_lines.append(f"<li><strong>{word}</strong> &mdash; {meaning}<br/><em>{phrase}</em><br/><em>{media}</em></li>")

    html_lines.append("</ul>")
    html_lines.append("</body></html>")

    plain = "\n".join(lines)
    html = "\n".join(html_lines)
    return plain, html


def view_trigger_standalone(number_of_words=3, hold_time=10):
    """
    Standalone version that opens HTML in browser without Streamlit.
    
    Args:
        number_of_words: Number of words to display
        hold_time: Seconds to display each word (only applies when auto-advancing)
    """
    selected_words = select_words_from_vocabulary(
        number_of_words=number_of_words, 
        selection_method="random", 
        current_level=1, 
        seq_no=1
    )
    
    if not selected_words:
        print("선택된 단어가 없습니다.")
        return
    
    print(f"📖 Displaying {len(selected_words)} words in browser...")
    
    # Create temp directory for HTML files
    temp_dir = tempfile.mkdtemp(prefix="vocab_viewer_")
    html_files = []
    
    # Generate HTML file for each word
    for idx, word in enumerate(selected_words):
        print(f"Selected word {idx+1}/{len(selected_words)}: {word.get('word', '')}")
        html_content = json_to_vocabulary_html(word)
        
        # Save to temp file
        html_file = os.path.join(temp_dir, f"word_{idx+1}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        html_files.append(html_file)
    
    # Open each HTML file in browser with delay
    for idx, html_file in enumerate(html_files):
        print(f"Opening word {idx+1}/{len(html_files)} in browser...")
        webbrowser.open('file://' + os.path.abspath(html_file))
        
        if idx < len(html_files) - 1:  # Don't sleep after last word
            time.sleep(hold_time)
    
    print("✨ 모든 단어가 재생되었습니다")
    print(f"💡 HTML files saved in: {temp_dir}")
    return html_files


async def view_trigger(words=None, to_addr=None):
    """
    Streamlit version - requires Streamlit to be running.
    """
    if not STREAMLIT_AVAILABLE:
        print("⚠️  Streamlit not available. Using standalone mode...")
        view_trigger_standalone()
        return
    
    selected_words = select_words_from_vocabulary(
        number_of_words=3, 
        selection_method="random", 
        current_level=1, 
        seq_no=1
    )
    hold_time = 10  # seconds to hold each display
    
    if selected_words:
        # Display all selected words sequentially
        for idx, word in enumerate(selected_words):
            print(f"Selected word {idx+1}/{len(selected_words)}: {word}")
            html_content = json_to_vocabulary_html(word)
            # Use scrolling=True to allow iframe to scroll and enable autoplay
            st.components.v1.html(html_content, height=420, scrolling=True)
            time.sleep(hold_time)  # Display content for specified seconds
        
        # Keep display - don't auto-complete, wait for manual button press
        print("✨ 모든 단어가 재생되었습니다")
    else:
        print("선택된 단어가 없습니다.")
        

# Main execution for standalone usage
if __name__ == "__main__":
    
    # Streamlit mode
    st.title("📖 Vocabulary Viewer")
    st.header("View selected words with audio")
    
    if st.button("View Today's Words"):
        asyncio.run(view_trigger())
    
    