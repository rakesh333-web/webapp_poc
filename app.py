
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
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }
    
    # Payload for the request
    payload = {
      "messages": [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and code generation tasks. You provide clear, precise instructions and code snippets for users to execute their tests in c++ "
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text":  z
            }
          ]
        }
      ],
      "temperature": 0,
      "top_p": 0.1,
      "max_tokens": 800
    }
    
    ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/gpt-4odeployment/chat/completions?api-version=2024-02-15-preview"
    
    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")
    
    # Handle the response as needed (e.g., print or process)
    result=response.json()
    
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
            promtg = ""
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
