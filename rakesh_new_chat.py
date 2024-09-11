import os
import requests
import base64
import streamlit as st

# Configuration
API_KEY = ""
IMAGE_PATH = "YOUR_IMAGE_PATH"
encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are an AI assistant that helps people for code generation"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV)"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Certainly! Here's a generic example of how you might write this in a programming environment designed for instrument control. Since you didn't specify a particular programming language or instrument, I'll provide a pseudo-code example:\n\n```pseudo\n// Initialize the power supply instrument\nps_initialize()\n\n// Set all pins to 0V\nps_set_voltage(all_pins, 0.0)\nps_set_current_limit(all_pins, current_limit) // Set an appropriate current limit\nps_output_enable(all_pins)\n\n// Force current on the pin of interest (LED2)\nps_set_current(LED2, -0.010) // Force -0.010 mA\nps_set_voltage_limit(LED2, voltage_limit) // Set an appropriate voltage limit\nps_output_enable(LED2)\n\n// Measure voltage on the pin of interest (LED2)\nvoltage_LED2 = ps_measure_voltage(LED2)\n\n// Output the measured voltage\nprint(voltage_LED2)\n\n// Disable output and reset the pin of interest (LED2)\nps_output_disable(LED2)\nps_set_current(LED2, 0.0)\nps_set_voltage(LED2, 0.0)\n\n// Finalize the power supply instrument\nps_finalize()\n```\n\nYou'll need to replace the pseudo-code functions with actual functions from your instrument's API/library. If you have a specific instrument or programming environment in mind, please provide more details for a more tailored example."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "no this is the correct code   //Force current and Measure result on PUT and store in variable"
        },
        {
          "type": "text",
          "text": "\n"
        },
        {
          "type": "text",
          "text": "psforce(LED2, PS_I, -0.010, PS_3p6V, PS_1MA)"
        },
        {
          "type": "text",
          "text": "psforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA)psmes(LED2, PSMES_V, 10, 10)"
        },
        {
          "type": "text",
          "text": "logres(results_LED2)"
        },
        {
          "type": "text",
          "text": "psverify(results_LED2, -1.0, 0.2)"
        },
        {
          "type": "text",
          "text": "psforce(LED2, PS_I, 0.0, PS_3p6V, PS_1MA)"
        },
        {
          "type": "text",
          "text": "psforce(LED2, PS_V, 0.0, PS_3p6V, PS_1MA)"
        },
        {
          "type": "text",
          "text": "\n"
        },
        {
          "type": "text",
          "text": "\n"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "It looks like you're using a specific API for instrument control. Here's a breakdown of the code you provided:\n\n```plaintext\n// Force current and Measure result on PUT and store in variable\npsforce(LED2, PS_I, -0.010, PS_3p6V, PS_1MA)  // Force -0.010 mA on LED2\npsforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA) // Set all pins to 0V\npsmes(LED2, PSMES_V, 10, 10)                  // Measure voltage on LED2\nlogres(results_LED2)                          // Log the results\npsverify(results_LED2, -1.0, 0.2)             // Verify the results within a range\npsforce(LED2, PS_I, 0.0, PS_3p6V, PS_1MA)     // Reset current on LED2 to 0\npsforce(LED2, PS_V, 0.0, PS_3p6V, PS_1MA)     // Reset voltage on LED2 to 0\n```\n\n### Explanation:\n\n- `psforce(LED2, PS_I, -0.010, PS_3p6V, PS_1MA)`: Forces a current of -0.010 mA on `LED2` with voltage and current limits.\n- `psforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA)`: Forces 0V on all pins with voltage and current limits.\n- `psmes(LED2, PSMES_V, 10, 10)`: Measures the voltage on `LED2`.\n- `logres(results_LED2)`: Logs the measured results.\n- `psverify(results_LED2, -1.0, 0.2)`: Verifies the results against expected values (-1.0 to 0.2).\n- `psforce(LED2, PS_I, 0.0, PS_3p6V, PS_1MA)`: Sets the current on `LED2` back to 0.\n- `psforce(LED2, PS_V, 0.0, PS_3p6V, PS_1MA)`: Sets the voltage on `LED2` back to 0.\n\nMake sure to adjust the parameters as needed for your specific application and instrument setup."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test LED2 and measure the voltage (MV)"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "// Force current and Measure result on PUT and store in variable\npsforce(LED2, PS_I, -0.010, PS_3p6V, PS_1MA)\npsforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA)\npsmes(LED2, PSMES_V, 10, 10)\nlogres(results_LED2)\npsforce(LED2, PS_I, 0.0, PS_3p6V, PS_1MA)\npsforce(LED2, PS_V, 0.0, PS_3p6V, PS_1MA)"
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}

ENDPOINT = "https://genainorthcentralus.openai.azure.com/openai/deployments/gpt-4odeployment/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
st.write(response.json())
