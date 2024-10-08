
import streamlit as st
import pandas as pd
import re
import string
import os
import requests
import base64
from rag import system_message

# Function to convert each row in the dataframe
def convert(row):
    s = row['Pin of Interest']
    v = row[s]
    #using APU32 instrument, force all pins to 0V and then Force -199.9 mA to the pin under test ETS and measure the voltage (MV)? set voltage and current to 0      measure the voltage (MV) and compare the results are in between -3.5V to 1.2V
    #Use the PS instrument. Force -0.010 mA current to LED2 pin and force 0.0V to all the pins. Measure voltage on LED2 pin and verify that measured voltage value is in between -1V to 0.2V. 
    return f"using APU32 instruments,force all pins to 0V and then Force {v} to the pin under test {s} pin and measure the voltage (MV) and compare the results are in between {row['Lower Limit']}V to {row['Upper Limit']}V,set voltage and current to 0 ."

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
              "text": """You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and code generation tasks. You provide clear, precise instructions and code snippets for users to execute their tests Below are help files of functions apu32set(), apu32mi(), apu32,mv, lwait(), & groupgetresults() followed by its functions, parameters, refer this for better generation, & use this for commenting purpose"""+ str(system_message)
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
      "temperature": 0.7,
      "top_p": 0.95,
      "max_tokens": 800
    }
    
    ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/GPT4-O-ATE/chat/completions?api-version=2024-02-15-preview"
    
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
    st.sidebar.image(image_url,width=300)
    
    st.title("ATE TEST CODE GENERATION")
    uploaded_f = st.sidebar.file_uploader("Upload your Excel file", type=["csv"])
    if uploaded_f is not None:
        try:
            df = pd.read_csv(uploaded_f)
            # Display original dataframe
            st.subheader("ORIGINAL TEST CASE FILE")
            st.dataframe(df)

            # Convert dataframe to English sentences
            df['english sentence'] = df.apply(convert, axis=1)

            # Display dataframe with English conversion
            st.subheader("ORIGINAL TEST CASES WITH ENGLISH CONVERSION")
            st.dataframe(df['english sentence'])

            # Add prefix to English sentences
            promtg = ""
            df['english sentence'] = df['english sentence'].apply(lambda x: promtg + x)

            # Process selected model
            
            st.subheader("INTERACTION WITH MODEL")
            x = process_client(df)
            # Display final translated and cleaned output
            st.subheader("GENERATED CODE IN C++")
        
            result_list = [x]  
            st.dataframe(result_list)   

        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

if __name__ == '__main__':
    main()
