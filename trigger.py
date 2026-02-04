"""
trigger.py - Trigger vocabulary viewer

Usage (standalone - no Streamlit required):
  python trigger.py

Usage (Streamlit mode):
  streamlit run trigger.py
"""
import logging
import os
import sys
from datetime import datetime

# Add parent directory to path so we can import viewer
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from viewer import view_trigger_standalone

# Change to script directory to ensure relative paths work
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Setup logging to project root
log_file = os.path.join(script_dir, 'trigger_log.txt')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Try to import streamlit

import streamlit as st
STREAMLIT_AVAILABLE = True

if __name__ == "__main__":
    logging.info("=== Vocabulary Viewer Trigger Started ===")
    
    
    # Streamlit mode
    logging.info("Running in Streamlit mode")
    st.title("📖 Vocabulary Trigger")
    st.write("Loading today's words with audio...")
    
    import asyncio
    from viewer import view_trigger
    asyncio.run(view_trigger())

    
    logging.info("=== Vocabulary Viewer Trigger Completed ===\n")