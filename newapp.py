import os
import streamlit as st

from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

# Replace with your Azure OpenAI credentials
api_key = "b5d5b5ea2ebd471b88b631a34ab7d52"
endpoint = "https://genainorthcentralus.openai.azure.com/"

# Create the OpenAI client
client = OpenAIClient(endpoint, AzureKeyCredential(api_key))

# Define the request parameters
response = client.chat_completions.create(
    deployment_id="gpt-4odeployment",  # or your specific deployment ID
    messages=[
        {"role": "system", "content": "You are an AI assistant that helps with code generation."},
        {"role": "user", "content": "code for the using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV)"}
    ],
    temperature=0.7,
    top_p=0.95,
    max_tokens=800
)
st.title("gpt code generations")
# Extract and print the response
generated_code = response.choices[0].message.content
st.write(generated_code)
