import os
import requests
import base64

# Configuration
API_KEY = "YOUR_API_KEY"
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
          "text": "You are an AI assistant for code generation. "
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
print(response.json())
