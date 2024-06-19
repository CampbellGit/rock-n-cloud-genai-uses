
import streamlit as st
import image_analyze_lib as glib

st.set_page_config(layout="wide", page_title="Image Understanding")

st.title("Image Analysis")

col1, col2, col3 = st.columns(3)

prompt_options_dict = {
    "Other": "",
}

prompt_options = list(prompt_options_dict)

image_options_dict = {
    "Other": "house.jpg"
    #Create sample post it picture
}

image_options = list(image_options_dict)


with col1:
    st.subheader("Select an Image")

    image_selection = st.radio("Please choose a picture:", image_options)
    
    if image_selection == 'Other':
        uploaded_file = st.file_uploader("Select an image", type=['png', 'jpg'], label_visibility="collapsed")
    else:
        uploaded_file = None
    
    if uploaded_file and image_selection == 'Other':
        uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_file.getvalue())
        st.image(uploaded_image_preview)
    #else:
    #    st.image(image_options_dict[image_selection])
    
    
with col2:
    st.subheader("Prompt")
    
    prompt_selection = st.radio("Prompt example:", prompt_options)
    
    prompt_example = prompt_options_dict[prompt_selection]
    
    prompt_text = st.text_area("Prompt",
        #value=,
        value=prompt_example,
        height=100,
        help="What you want to know about the image.",
        label_visibility="collapsed")
    
    go_button = st.button("Go", type="primary")
    
    
with col3:
    st.subheader("Result")

    if go_button:
        with st.spinner("Processing..."):
            
            if uploaded_file:
                image_bytes = uploaded_file.getvalue()
            else:
                image_bytes = glib.get_bytes_from_file(image_options_dict[image_selection])
            
            response = glib.get_response_from_model(
                prompt_content=prompt_text, 
                image_bytes=image_bytes,
            )
        
        st.write(response)
