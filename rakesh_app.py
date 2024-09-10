import requests
import streamlit as st
st.title("gpt responce")

# Replace with your Azure OpenAI API key and endpoint
API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d52"
ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/gpt-4odeployment/chat/completions?api-version=2024-02-15-preview"

# Define headers for API requests
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

# Define the payload for the API request
payload = {
    "messages": [
        {"role": "system", "content": "You are an AI assistant that helps with code generation."},
        {"role": "user", "content": "code for the using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV)"}
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
}

# Make the API request
response = requests.post(ENDPOINT, headers=headers, json=payload)

# Check for request errors
response.raise_for_status()

# Extract and print the response
result = response.json()
generated_code = result.get('choices', [{}])[0].get('message', {}).get('content', 'No code generated.')
st.write(generated_code)
