import streamlit as st
st.title("gpt responce")
model_name = "gpt-4odeployment"
#llm = ChatOpenAI(model_name=model_name)
from llama_index.llms.azure_openai import AzureOpenAI
llm = AzureOpenAI(
    engine=model_name,
    temperature=0.0,
    azure_endpoint="https://genainorthcentralus.openai.azure.com/",
    api_key="b5d5b5ea2ebd471b88b631a34ab7d52",
    api_version="2024-02-15-preview"
)
response = llm.complete("code for the using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV)")
st.write(response)
