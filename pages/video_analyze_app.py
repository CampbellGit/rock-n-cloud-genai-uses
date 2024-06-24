
import streamlit as st
import video_analyze_lib as glib
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

st.set_page_config(layout="wide", page_title="Video Analysis")

st.title("Video Analysis")

col1, col2 = st.columns(2)

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
    st.subheader("Select a Video")

    image_selection = st.radio("Please choose a video:", image_options)
    
    if image_selection == 'Other':
        uploaded_file = st.file_uploader("Select an video", type=['png', 'jpg'], label_visibility="collapsed")
    else:
        uploaded_file = None
    
    if uploaded_file and image_selection == 'Other':
        uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_file.getvalue())
        st.image(uploaded_image_preview)
    #else:
    #    st.image(image_options_dict[image_selection])
    go_button = st.button("Go", type="primary")

    
    
with col2:
    st.subheader("Result")
 
    if go_button:
        #use an empty container for streaming output
        with st.spinner("Streaming..."):
            st_callback = StreamlitCallbackHandler(st.container())
            streaming_response = glib.get_response_from_model()
             # Handle the streaming response
            full_text = ""
            response_placeholder = st.empty()  # Create a placeholder for dynamic content

            for chunk in streaming_response:
                full_text += chunk  # Accumulate chunks of streamed data
                response_placeholder.text(full_text)  # Update the placeholder with new content
              
        st.download_button(label= "Download here", data= full_text)