import os
import requests
import pandas as pd
from rag import system_message

# Configuration
API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d522"  # Replace with your actual API key

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Load the Excel file
file_path = './test_input_data_426.xlsx'  # Update with the actual file path
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Ensure the Response column exists
if 'Response' not in df.columns:
    df['Response'] = ""

# Endpoint for API request
ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/GPT4-O-ATE/chat/completions?api-version=2024-02-15-preview"

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    updated_prompt = row['prompt'] + " set current and voltage to 0"
    
    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and c++ code generation tasks. You provide clear, precise instructions and code snippets for users to execute their tests Below are help files of functions apu32set(), apu32mi(), apu32,mv, lwait(), & groupgetresults() followed by its functions, parameters, refer this for better generation, & use this for commenting purpose"""+ str(system_message)+"""Following are the instructions to be followed for specific range of values For Current Range 10 μA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [15 μA] / 75% [7.5 μA] / 35% [3.5 μA], For Current Range 100 μA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [150 μA] / 75% [75 μA] / 35% [35 μA], For Current Range 1 mA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [1.5 mA] / 75% [750 μA] / 35% [350 μA], For Current Range 10 mA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [15 mA] / 75% [7.5 mA] / 35% [3.5 mA], For Current Range 50 mA use Voltage Range 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [65 mA] / 60% [30 mA] / N/A, For Current Range 100 mA use Voltage Range 3.6 V, 10 V, 30 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [130 mA] / 60% [60 mA] / 20% [20 mA], For Current Range 200 mA use Voltage Range 3.6 V, 10 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [260 mA] / 60% [120 mA] / 20% [40 mA]. make sure valid voltage range is between 81 V and -81 V and valid current range is between 201 mA and -201 mA if it is above range return 'voltage or current is beyond permitted range please correct'"""
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

    # Sending request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the request was unsuccessful

        # Extracting the code content from the API response
        json_data = response.json()
        code_content = json_data['choices'][0]['message']['content']
        
        # Update the response column with the generated code_content
        df.at[index, 'Response'] = code_content  # Update the current row's response column
        
        # Print the success message
        print(f"Response {index + 1} is updated.")

    except requests.RequestException as e:
        print(f"Failed to make the request for row {index}. Error: {e}")
        df.at[index, 'Response'] = "Error in request"

# Save the updated DataFrame back to the Excel file
output_path = 'finetuning_test_evaluation_426_3_10_2024_updated_system_message.xlsx'
df.to_excel(output_path, index=False)

print(f"Excel file updated and saved as {output_path}")
