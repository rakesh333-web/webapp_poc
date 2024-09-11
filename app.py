
import streamlit as st
import pandas as pd

import re
import string
import os
import requests
import base64

# Function to convert each row in the dataframe
def convert(row):
    s = row['Pin of Interest']
    v = row[s]
    #Use the PS instrument. Force -0.010 mA current to LED2 pin and force 0.0V to all the pins. Measure voltage on LED2 pin and verify that measured voltage value is in between -1V to 0.2V. 
    return f"using ps instrument.Force {v} on {s} pin and force 0.0V to all the pins.measure the voltage on the same {s} pin and verify that measured voltage value is in between {row['Lower Limit']} and {row['Upper Limit']}."

# Function to clean text


# Function to translate text to English


# Initialize Hugging Face clients

def process_client(df):
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
                        "text": z
                    }
                ]
            }
        ],
        "temperature": 0.01,
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
    content = result.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
    return content
   

def main():
    st.set_page_config(layout="wide", page_title="MODELS")

    # Sidebar UI for uploading file and selecting model
    image_url = "./images.png"
    st.title("ATE Test code Generation")
    st.sidebar.image(image_url, width=300)
    uploaded_f = st.sidebar.file_uploader("Upload your Excel file", type=["csv"])
    

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
            promtg = "generate c++ code "
            df['english sentence'] = df['english sentence'].apply(lambda x: promtg + x)

            # Process selected model
            
            st.subheader("Interact with Model")
            x = process_client(df)
            

            
            

            # Display final translated and cleaned output
            st.subheader("Final Output")
            st.write(x)

        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

if __name__ == '__main__':
    main()
