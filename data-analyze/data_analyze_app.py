import streamlit as st
import data_analyze_lib as glib

st.set_page_config(layout="wide", page_title="Data Analysis")

st.title("Data Analysis")

col1, col2, col3 = st.columns(3)

prompt_options_dict = {
    "JSON": """Analyze this list and output it as a JSON, for cities, add the postal code.
        Here's an example:
        [
        {"nom": string,
        "prenom": string,
        "age": number,
        "adresse": string,
        "ville": string,
        "code_postal": number
        }]""",
    "Table": "Analyze this list and output it as a CSV"
}

prompt_options = list(prompt_options_dict)



with col1:
    input_text = st.text_area("Search for:")
    
    
with col2:
    st.subheader("Prompt")
    
    prompt_selection = st.radio("Prompt example:", prompt_options)
    
    prompt_example = prompt_options_dict[prompt_selection]
    
    prompt_text = st.text_area("Prompt",
        #value=,
        value=prompt_example,
        height=100,
        help="What you want to know about the list.",
        label_visibility="collapsed")
    
    go_button = st.button("Go", type="primary")
    
    
with col3:
    st.subheader("Result")
            
    if go_button: #code in this if block will be run when the button is clicked
        with st.spinner("Running..."): #show a spinner while the code in this with block runs
            input=prompt_text+input_text
            has_error, response_content, err = glib.get_json_response(input_content=input) #call the model through the supporting library

        if not has_error:
            st.json(response_content) #render JSON if there was no error
        else:
            st.error(err) #otherwise render the error
            st.write(response_content) #and render the raw response from the model