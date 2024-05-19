import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from response_utils import *
import logging

# Render the Image Playgroud tab with mutile child tabs
def render_image_playground_tab(multimodal_model_pro: GenerativeModel):
    st.write("Using Gemini 1.0 Pro Vision - Multimodal model")
    recommendations, screen, diagrams, equations = st.tabs(["Further recommendations", "Oven instruction", "ER Diagrams", "Math Reasoning"])

    with recommendations:
        room_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/living_room.jpeg"
        chair_1_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair1.jpeg"
        chair_2_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair2.jpeg"
        chair_3_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair3.jpeg"
        chair_4_image_uri = "gs://cloud-training/OCBL447/gemini-app/images/chair4.jpeg"

        room_image_url = "https://storage.googleapis.com/"+room_image_uri.split("gs://")[1]
        chair_1_image_url = "https://storage.googleapis.com/"+chair_1_image_uri.split("gs://")[1]
        chair_2_image_url = "https://storage.googleapis.com/"+chair_2_image_uri.split("gs://")[1]
        chair_3_image_url = "https://storage.googleapis.com/"+chair_3_image_uri.split("gs://")[1]
        chair_4_image_url = "https://storage.googleapis.com/"+chair_4_image_uri.split("gs://")[1]        

        room_image = Part.from_uri(room_image_uri, mime_type="image/jpeg")
        chair_1_image = Part.from_uri(chair_1_image_uri,mime_type="image/jpeg")
        chair_2_image = Part.from_uri(chair_2_image_uri,mime_type="image/jpeg")
        chair_3_image = Part.from_uri(chair_3_image_uri,mime_type="image/jpeg")
        chair_4_image = Part.from_uri(chair_4_image_uri,mime_type="image/jpeg")

        st.image(room_image_url, width=350, caption="Image of living room")
        st.image([chair_1_image_url, chair_2_image_url, chair_3_image_url, chair_4_image_url], width=200, caption=["Chair 1","Chair 2","Chair 3","Chair 4"])

        st.write("Our expectation: Recommed a chair that would complement the given image of a living room.")
        prompt_list = [ "Consider the following chairs: ",
                       "chair 1: ", chair_1_image,
                       "chair 2: ", chair_2_image,
                       "chair 3: ", chair_3_image, "and",
                       "chair 4: ", chair_4_image, "\n",
                       "For each chair, explain why it would be suitable or not suitable for the living room:",
                       room_image,
                       "Only recommend for the room provided and not other rooms. Provide your recommendation in a table format with chair name and reason as columns.",
        ]

        tab1, tab2 = st.tabs(["Response", "Prompt"])
        generate_image_description = st.button("Generate recommendation", key="generate_image_description")

        with tab1:
            if generate_image_description and prompt_list:
                with st.spinner("Generating recommendation using Gemini..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro, prompt_list)
                    st.markdown(response)
                    logging.info(response)

        with tab2:
            st.write("Prompt used:")
            st.text(prompt_list)

    with screen:
        oven_screen_uri = "gs://cloud-training/OCBL447/gemini-app/images/oven.jpg"
        oven_screen_url = "https://storage.googleapis.com/"+oven_screen_uri.split("gs://")[1]
        oven_screen_image = Part.from_uri(oven_screen_uri, mime_type="image/jpeg")

        st.image(oven_screen_url, width=350, caption="Image of oven control panel")
        st.write("Provide instructions for resetting the clock on this appliance in English")

        prompt = """How can I reset the clock on this appliance? Provide the instructions in English.
                If instructions include buttons, also explain where those buttons are physically located.
                """
        
        tab1, tab2 = st.tabs(["Response", "Prompt"])
        generate_instruction_description = st.button("Generate instructions", key="generate_instruction_description")

        with tab1:
            if generate_instruction_description and prompt:
                with st.spinner("Generating instructions using Gemini..."):
                    response = get_gemini_pro_vision_response(multimodal_model_pro, [oven_screen_image ,prompt])
                    st.markdown(response)
                    logging.info(response)

        with tab2:
            st.write("Prompt used:")
            st.text(prompt+"\n"+"input_image")

    