import os
import requests
import base64
import streamlit as st
API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d522"
z="Use the PS instrument. Force -0.010 mA current to LED2 pin and force 0.0V to all the pins. Measure voltage on LED2 pin and verify that measured voltage value is in between -1V to 0.2V. "
st.title("gpt responce")
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
content = result.get('choices', [{}])[0].get('message', {}).get('content', 'No content found')
st.write(content)  




 

