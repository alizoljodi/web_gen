import streamlit as st
import streamlit.components.v1 as components
import time
import random
import os
import tempfile
import webbrowser
from datetime import datetime
import json
import groq
from controller import AppController

# Create and run the application
if __name__ == "__main__":
    app = AppController()
    app.run()
