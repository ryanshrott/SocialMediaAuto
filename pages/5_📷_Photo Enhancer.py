import os
import streamlit as st
from PIL import Image
import requests
import io
import pathlib
import replicate
import zipfile
from io import BytesIO

st.set_page_config(page_title="SmartBids", page_icon=":house", layout="centered", initial_sidebar_state="auto", menu_items=None)

os.environ["REPLICATE_API_TOKEN"] = os.environ.get("REPLICATE_API_TOKEN")

st.title('Convert photos to DSLR quality')

uploaded_files = st.file_uploader("Select a photo",  type = (["jpg", "jpeg", "png", "JPEG"]), accept_multiple_files=True)

output_files = []

if st.button('Enhance') and uploaded_files:
    c1, c2 = st.columns(2)
    
    with c1:
        for i, file in enumerate(uploaded_files):
            image = Image.open(file)
            st.image(image, caption=f'no enhancement - image {i+1}')

    with c2:
        for i, file in enumerate(uploaded_files):
            inputs = {
                'image': file,
                'upscale': 4,
            }

            def get_response(inputs):
                return replicate.run(
                    "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
                    input=inputs,
                )
            enhanced_image_url = get_response(inputs)
            
            # Convert the response content (URL) to an image
            enhanced_image = Image.open(BytesIO(requests.get(enhanced_image_url).content))

            output_filename = file.name.split('.')[0] + '_ENHANCED.PNG'
            enhanced_image.save(output_filename)
            st.image(enhanced_image, caption=f'enhanced - image {i+1}')
            output_files.append(output_filename)

if len(output_files) > 0:
    # create a zip file of all the output files
    zip_filename = 'enhanced_images.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zip:
        for file in output_files:
            zip.write(file)

    # Read the created zip file as bytes
    with open(zip_filename, 'rb') as f:
        zip_data = f.read()

    # download the zip file
    st.download_button(
        label="Download Enhanced Images as Zip",
        data=zip_data,
        file_name=zip_filename,
        mime="application/zip"
    )
