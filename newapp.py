import os
import streamlit
from openai import AzureOpenAI
    
client = AzureOpenAI(
  azure_endpoint = "https://genainorthcentralus.openai.azure.com/", 
  api_key=os.getenv("b5d5b5ea2ebd471b88b631a34ab7d522"),  
  api_version="2024-02-01"
)
    
deployment_name='gpt-4odeployment'
    

st.title("GPT Responce")
start_phrase = 'code for the using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV) '
response = client.completions.create(
    model=deployment_name,
    prompt=start_phrase,
    max_tokens=100,
    top_p=0.5,
    frequency_penalty=0,
    presence_penalty=0,
    best_of=1,
    stop=None
) 
st.write(response.choices[0].text)
