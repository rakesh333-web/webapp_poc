from huggingface_hub import InferenceClient
import streamlit as st
import pandas as pd
from googletrans import Translator
import re
import string
import os
import requests
import base64

# Function to convert each row in the dataframe
def convert(row):
    s = row['Pin of Interest']
    v = row[s]
    return f"Force {v} on {s} pin and measure the voltage on the same {s} pin with SPU with range of {row['Lower Limit']} and {row['Upper Limit']}."

# Function to clean text
def clean_text(text):
    printable_text = ''.join(char for char in text if char in string.printable)  # Remove non-printable characters
    cleaned_text = re.sub(r'[^\x00-\x7F]', '', printable_text)  # Remove non-ASCII characters
    return cleaned_text

# Function to translate text to English
def translate_to_english(text, src_lang='auto'):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest='en')
    return translation.text

# Initialize Hugging Face clients
vishesh_client = InferenceClient("imvishesh007/gemma-Code-Instruct-Finetune-test",token="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")
madhavi_client = InferenceClient("imvishesh007/gemma-Code-Instruct-Finetune-test",token="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")
rakesh_client = InferenceClient("bandi333/gemma-Code-Instruct-Finetune-test-v0.0",token="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")
models = {
    "vishesh_client": vishesh_client,
    "rakesh_client": rakesh_client,      # Add your token and model for rakesh_client if needed
    "madhavi_client": madhavi_client      # Add your token and model for madhavi_client if needed
}
def process_client(client, df):
    x = ""
    options = df['english sentence'].tolist()
    z = st.radio('Select a sentence:', options)
    API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d522"

    # Define the headers for the API request
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    # Define the payload for the API request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",  # Ensure 'type' is correctly defined as 'text'
                        "text": "You are an AI assistant that helps people find information."
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }
    
    # Define the API endpoint
    ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/gpt-4odeployment/chat/completions?api-version=2024-02-15-preview"
    
    # Make the API request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
    # Handle the response as needed (e.g., print or process)
    result = response.json()
    return result  # Print the response to check the output

    """
    if z:
        for message in client.chat_completion(messages=[{"role": "user", "content": z}], max_tokens=500, stream=True):
            x += message.choices[0].delta.content

    return x
    """
    """
    x = ""
    for i in range(df.shape[0]):
        z = st.checkbox(df['english sentence'][i])
        if z:
            for message in client.chat_completion(messages=[{"role": "user", "content": df['english sentence'][i]}], max_tokens=500, stream=True):
                print(message.choices[0].delta.content, end="")
                x += message.choices[0].delta.content
    return x
    """

def main():
    st.set_page_config(layout="wide", page_title="MODELS")

    # Sidebar UI for uploading file and selecting model
    image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfM34DG2u5fZI_pslFvrMpPKNNRBtbknBlVg&s"
    st.title("ATE Test code Generation")
    st.sidebar.image(image_url, width=200)
    uploaded_f = st.sidebar.file_uploader("Upload your Excel file", type=["csv"])
    selected_model = st.sidebar.selectbox("Choose your model", options=list(models.keys()))

    if uploaded_f is not None:
        try:
            df = pd.read_csv(uploaded_f)

            # Display original dataframe
            st.subheader("Original Test Case File")
            st.dataframe(df)

            # Convert dataframe to English sentences
            df['english sentence'] = df.apply(convert, axis=1)

            # Display dataframe with English conversion
            st.subheader("Dataframe with English Conversion")
            st.dataframe(df['english sentence'])

            # Add prefix to English sentences
            promtg = "code for the given requirement using customlibrary in cpp for the pin configuration test case using psinstrument "
            df['english sentence'] = df['english sentence'].apply(lambda x: promtg + x)

            # Process selected model
            if selected_model in models and models[selected_model] is not None:
                st.subheader("Interact with Hugging Face Model")
                x = process_client(models[selected_model], df)
            else:
                st.warning(f"Model {selected_model} is not configured or available.")

            # Translate and clean the final output
            x = translate_to_english(x)
            x = clean_text(x)

            # Display final translated and cleaned output
            st.subheader("Final Translated and Cleaned Output")
            st.write(x)

        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

if __name__ == '__main__':
    main()
