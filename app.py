import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key for Google Generative AI is not set. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Configure the Generative AI client
genai.configure(api_key=api_key)

def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating content: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        st.error("No file uploaded.")
        return None

# Initialize the Streamlit app
st.set_page_config(page_title="Calories Advisor App")

st.header("Calories Advisor App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image,
calculate the total calories, and provide details of each food item with calorie intake as follows:

1. Item 1 - number of calories
2. Item 2 - number of calories
...
Finally, mention whether the food is healthy or not, and provide the percentage split of carbohydrates, fats, fibers, sugars, and other important dietary components.
"""

if st.button("Tell me about the total calories:"):
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        if image_data:
            response = get_gemini_response(input_prompt, image_data)
            if response:
                st.header("The Response is:")
                st.write(response)
    else:
        st.error("Please upload an image to proceed.")
