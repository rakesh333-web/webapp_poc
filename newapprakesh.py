import os
import requests
import base64

# Configuration
API_KEY = "YOUR_API_KEY"
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
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "//Force current and Measure result on PUT and store in variable \npsforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA);//All_pins=Pin of interest, Ps_v=Power supply mode,0.0=Force value, V range, I range\npsforce(LED2, PS_I, -0.010, PS_3p6V, PS_1MA);//LED2=Pin of interest, PS_I=Power supply mode, -0.010 = Force value, V range, I range\npsmes(LED2, PSMES_V, 10, 10);//LED2=Pin of interest, PSMES_V= Voltage measure mode, no. of sample, sample delay between each sample\nlogres(results_LED2);// Result store  and Datalog\npsforce(LED2, PS_I, 0.0, PS_3p6V, PS_1MA);//LED2=Pin of interest, PS_I=Power supply mode, 0.0 = Force value, V range, I range\npsforce(LED2, PS_V, 0.0, PS_3p6V, PS_1MA);//LED2=Pin of interest, PS_V=Power supply mode,0.0= Force value, V range, I range"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test AN and measure the voltage (MV)"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "//Force current and Measure result on PUT and store in variable \npsforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA);//All_pins=Pin of interest, Ps_v=Power supply mode,0.0= Force value, V range, I range\npsforce(AN, PS_I, -0.010, PS_3p6V, PS_1MA);//AN=Pin of interest, PS_I=Power supply mode, -0.010 = Force value, V range, I range\npsmes(AN, PSMES_V, 10, 10);//AN=Pin of interest, PSMES_V= Voltage measure mode, no. of sample, sample delay between each sample\nlogres(results_AN);// Result store  and Datalog\npsforce(AN, PS_I, 0.0, PS_3p6V, PS_1MA);//AN=Pin of interest, PS_I=Power supply mode, 0.0 = Force value, V range, I range\npsforce(AN, PS_V, 0.0, PS_3p6V, PS_1MA);//AN=Pin of interest, PS_V=Power supply mode,0.0= Force value, V range, I range"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "using PS instrument, force all pins to 0V and then Force -0.010 mA to the pin under test VE and measure the voltage (MV)"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "//Force current and Measure result on PUT and store in variable \npsforce(All_Pins, PS_V, 0.0, PS_3p6V, PS_1MA);//All_pins=Pin of interest, Ps_v=Power supply mode,0.0= Force value, V range, I range\npsforce(VE, PS_I, -0.010, PS_3p6V, PS_1MA);//VE=Pin of interest, PS_I=Power supply mode, -0.010 = Force value, V range, I range\npsmes(VE, PSMES_V, 10, 10);//VE=Pin of interest, PSMES_V= Voltage measure mode, no. of sample, sample delay between each sample\nlogres(results_VE);// Result store  and Datalog\npsforce(VE, PS_I, 0.0, PS_3p6V, PS_1MA);//VE=Pin of interest, PS_I=Power supply mode, 0.0 = Force value, V range, I range\npsforce(VE, PS_V, 0.0, PS_3p6V, PS_1MA);//VE=Pin of interest, PS_V=Power supply mode,0.0= Force value, V range, I range"
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
print(response.json())
