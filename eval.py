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

file_path = 'path_to_your_file.xlsx'  # Update with the actual file path

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

                    "text": """You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and code generation tasks. You provide clear, precise instructions and code snippets for users to execute their tests
Below are help files of functions apu32set(), apu32mi(), apu32,mv, lwait(), & groupgetresults() followed by its functions, parameters, refer this for better generation, & use this for commenting purpose
Function Name: lwait()
Description: This utility adds a programmed delay in the test program flow.
Parameters: delay
Returns: {"description": "None."}
Usage: The parameter delay is a long integer, which can cause a wait from a few microseconds to many seconds.

Function Name: apu32mi()
Description: This utility measures a current on the specified APU-32 pins and returns the current reading in milliamps.
Parameters: PinName, IGain, NumSamples, SampleDelay, Site
Returns: {"description": "This utility returns the average measured value in mA (status). If a failure occurs, it returns FLT_MAX.", "group_measurements": "For group measurements, the utility returns the value from the first APU-32 pin in a group. Use groupgetresults() to get the results from a group measurement.", "on_error": "See onerr() for a list of error codes."}
Usage: This utility returns the average of the current measurement readings. The NumSamples parameter sets the number of ADC triggers, and SampleDelay specifies the time interval between samples. Each APU-32 pin has its own ADC, so each pin can be clocked individually. The pin must be in a forcing mode.

Function Name: groupgetresults()
Description: This utility gets the measured results from the last measurement utility called that operated on a group of instruments.
Parameters: results, size
Returns: {"description": "The number of instrument results filled into the results array."}
Usage: {"description": "This utility returns measured values in the results parameter, which is a user-defined variable of the type RESULTS_STR. Each array element of this structure is filled with the appropriate data for each instrument in the group.", "results_str_definition": {"typedef": "struct", "structure": {"resource": "int - ISO-COMM position or pin number", "site": "int - site, 0-15, -1 if not assigned to a site, -2 if instrument is off", "value": "double - measured value, 0.0 if instrument is off", "PassFail": "int - Filled in by msLogDataAll(), +1, 0, -1, +2"}}, "example_declaration": "RESULTS_STR results[NUM_SITES * 8]; // NUM_SITES defined as 2 in .h file", "example_usage": ["// Set up the instrument and get the forcing value (Force_I) from the datasheet", "apu32set(APU_CONT, APU32_FI, Force_I[DSIndex], APU32_10V, APU32_1MA, APU32_PIN_TO_VI, APU32_KELVIN_OFF);", "// Take 8 measurements 10 microseconds apart and average the result", "apu32mv(APU_CONT, APU32_MV_1X, 1, 10, APU32_NOT_SHARED, APU32_NORMAL, MS_ALL);", "// Gather the measurements:", "groupgetresults(results, NUM_SITES * 8);"]}

Function Name: apu32set()
Description: This utility sets the mode, forcing value, voltage range, and current range for the specified pins. This utility also closes relays belonging to an APU-32 pin or group of pins. You must call this utility before calling other APU-32 utilities.
Parameters: PinBusList, Mode, Value, Vrange, Irange, Connect, ConnectMode, Site
Returns: {"description": "This utility returns an integer that indicates the result of a call (status).", "status_codes": ["0: Operation successful.", "Nonzero: Failure. See onerr() for a list of error codes."]}
Usage: Forcing voltage into a capacitive load can cause large overshoot and excessive ringing, resulting in long settling times. Enabling phase-lead compensation can reduce overshoot and ringing. This should be enabled only when a capacitive load is present.

Function Name: apu32mv()
Description: This utility measures voltage on the specified APU-32 pins and returns the voltage reading in volts.
Parameters: PinName, VGain, NumSamples, SampleDelay, IGainShared, Mode, Site
Returns: {"description": "This utility returns the average measured value in volts (value). If a failure occurs, it returns FLT_MAX.", "group_measurements": "For group measurements, the utility returns the value from the first APU-32 pin in a group. Use groupgetresults() to get the results from a group measurement.", "on_error": "See onerr() for a list of error codes."}
Usage: This utility returns the average of the voltage measurement readings, as defined by the NumSamples parameter, which sets the number of ADC triggers, and SampleDelay specifies the time interval between samples. Each APU-32 pin has its own ADC, so each pin can be clocked individually. The pin must be in a forcing mode." """
	

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
 
ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/GPT4-O-ATE/chat/completions?api-version=2024-02-15-preview"
 
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

output_path = 'updated_test_evaluation_432.xlsx'

df.to_excel(output_path, index=False)
 
print(f"Excel file updated and saved as {output_path}")

 
