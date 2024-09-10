
import os
from openai import AzureOpenAI
import streamlit as st

client = AzureOpenAI(
  azure_endpoint = (""),
  api_key = ("AZURE_OPENAI_API_KEY"),
  api_version = "2024-06-01"
)
st.title("gpt responce")
response = client.chat.completions.create(
    model = "", # model = "Custom deployment name you chose for your fine-tuning model"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

st.write(response.choices[0].message.content)
