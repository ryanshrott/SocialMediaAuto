import streamlit as st
import requests
import base64
import os
from PIL import Image
import io
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title='SEO Image Alt-Text Generator', layout='wide')

# Title and description
st.title('SEO Image Alt-Text Generator')
st.write('Upload an image to generate SEO-optimized alt text with keywords.')

# Function to encode the image
# Function to encode the image
def encode_image(image_file):
    image = Image.open(image_file)
    
    # Convert RGBA to RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')
        
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


# Image uploader
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Button to generate alt text
if st.button('Generate Alt Text'):
    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

        # Encode the uploaded image
        base64_image = encode_image(uploaded_image)

        # Prepare the headers and payload for the OpenAI API call
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"  # Use Streamlit secrets to store the API key
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Create detailed and appealing SEO-optimized ALT text for the real estate listing image provided. Incorporate relevant keywords such as 'luxury real estate,' 'spacious family home,' 'modern design,' and 'prime location' that potential homebuyers are likely to search for. Ensure the alt text accurately describes the visible elements in the image and conveys the atmosphere of the home, enhancing accessibility and search engine ranking for real estate listings."

                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Make the API call to generate the alt text
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        # Check the response and display the alt text
        if response.status_code == 200:
            data = response.json()
            alt_text = data['choices'][0]['message']['content']
            st.success(f"Generated Alt Text: {alt_text}")
        else:
            st.error("Error in generating alt text. Please check the image and try again.")
    else:
        st.error("Please upload an image to generate alt text.")

# Run the Streamlit app by using the command `streamlit run your_script.py`
