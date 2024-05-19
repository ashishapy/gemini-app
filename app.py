import os
import streamlit as st
from app_tab1 import rendor_story_tab
from app_tab2 import render_mktg_campaign_tab
from app_tab3 import render_image_playground_tab
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import logging
from google.cloud import logging as google_logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Attach a Google Cloud Logging handler to the root logger
log_client = google_logging.Client()
log_client.setup_logging()

PROJECT_ID = os.getenv('PROJECT_ID')
LOLCATION = os.getenv('REGION')
vertexai.init(project=PROJECT_ID, location=LOLCATION)

@st.cache_resource  # This will cache the data across runs
def load_models():
    text_model_pro = GenerativeModel('gemini-pro')
    multimodal_model_pro = GenerativeModel('gemini-pro-vision')
    return text_model_pro, multimodal_model_pro

st.header("Vertex AI Gemini AI", divider="rainbow")
text_model_pro, multimodal_model_pro = load_models()

tab1, tab2, tab3, tab4 = st.tabs(["Story", "Marketing Campaign", "Image Playground", "Video Playground"])

with tab1:
    rendor_story_tab(text_model_pro)

with tab2:
    render_mktg_campaign_tab(text_model_pro)

with tab3:
    render_image_playground_tab(multimodal_model_pro)