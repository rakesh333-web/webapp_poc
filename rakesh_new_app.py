
import os
from openai import AzureOpenAI
import streamlit as st

client = AzureOpenAI(
  azure_endpoint = "https://genainorthcentralus.openai.azure.com/",
  api_key = "b5d5b5ea2ebd471b88b631a34ab7d52",
  api_version = "2024-02-15-preview"
)
st.title("gpt responce")
response = client.chat.completions.create(
    model = "gpt-4odeployment", # model = "Custom deployment name you chose for your fine-tuning model"
    messages = [
        {"role": "system", "content": "You are an AI assistant that helps with code generation"},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

st.write(response.choices[0].message.content)
