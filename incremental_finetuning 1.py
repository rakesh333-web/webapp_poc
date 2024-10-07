import os

import requests

import base64

import pandas as pd
 
# Configuration

API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d522"
 
headers = {

    "Content-Type": "application/json",

    "api-key": API_KEY,

}
 
# Load the Excel file

file_path = './test_evaluation_432.xlsx'  # Update with the actual file path

df = pd.read_excel(file_path, sheet_name='Sheet1')
 
# Extract and append the string to the first 'prompt' for demonstration

updated_prompt = df['prompt'][0] + " set current and voltage to 0"
 
# Payload for the request

payload = {

    "messages": [

        {

            "role": "system",

            "content": [

                {

                    "type": "text",

                    "text": "You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and code generation tasks. You provide clear, precise instructions and code snippets for users to execute their tests."
                }

            ]

        },

        {

            "role": "user",

            "content": [

                {

                    "type": "text",

                    "text": updated_prompt  # Use the modified prompt

                }

            ]

        }

    ],

    "temperature": 0,

    "top_p": 0.95,

    "max_tokens": 800

}
 
ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/gpt-4o-2024-08-06-model1function/chat/completions?api-version=2024-02-15-preview"
 
# Sending request

try:

    response = requests.post(ENDPOINT, headers=headers, json=payload)

    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

except requests.RequestException as e:

    raise SystemExit(f"Failed to make the request. Error: {e}")
 
# Extracting the code content from the API response

json_data = response.json()

code_content = json_data['choices'][0]['message']['content']
 
# Update the response column with the generated code_content

df.at[0, 'Response'] = code_content  # Assuming updating for the first row only for now
 
# Save the updated DataFrame back to the Excel file

output_path = 'incremental_finetuning_test_evaluation_432.xlsx'

df.to_excel(output_path, index=False)
 
print(f"Excel file updated and saved as {output_path}")

 
