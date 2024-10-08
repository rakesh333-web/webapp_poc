import os
import requests
import re
import openai
import json
import chromadb


# Azure OpenAI Configuration
API_KEY = "b5d5b5ea2ebd471b88b631a34ab7d522"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# ChromaDB initialization
openai.api_type = "azure"
openai.api_base = "https://genaifinetuning.openai.azure.com/"
openai.api_version = "2023-05-15"
openai.api_key = "a27d6ecbcedd487bb0499af0b6544676"

client = chromadb.Client()

# Step 1: Store data into ChromaDB
def store_data_in_chromadb():
    """
    This function stores function metadata from a JSON file into ChromaDB with embeddings.
    """
    # Check if the collection exists and get or create.
    collection = client.get_or_create_collection("apu32_functions_in_detail")

    # Load JSON data
    with open('./vectordb_data.json', 'r') as f:
        data = json.load(f)

    # Iterate over each function, generate embeddings, and store in Chroma DB
    for i, item in enumerate(data):  # Use enumerate to get unique IDs for each function
        # Convert the 'description' field to embeddings
        response = openai.Embedding.create(
            input=item["description"],
            engine="ate-test-embedding-ada"  # Specify the Azure model
        )

        # Extract the embedding from the response
        embedding = response['data'][0]['embedding']

        # Convert the list fields like 'parameters', 'availability', 'examples', etc., into strings
        parameters_str = ', '.join([param["name"] for param in item.get("parameters", [])])
        availability_str = ', '.join(item.get("availability", []))  # Join availability array into a string

        examples = item.get("examples", {})
        examples_str = (
            f"description: {examples.get('description', 'N/A')}, code: {examples.get('code', 'N/A')}"
            if isinstance(examples, dict)
            else "N/A"
        )

        returns_str = json.dumps(item.get("returns", {})) if isinstance(item.get("returns"), dict) else str(item.get("returns"))
        usage_str = json.dumps(item.get("usage", {})) if isinstance(item.get("usage"), dict) else str(item.get("usage", "N/A"))
        declarations_str = json.dumps(item.get("declarations", {})) if isinstance(item.get("declarations"), dict) else str(item.get("declarations", "N/A"))

        # Store in ChromaDB with all relevant metadata
        collection.add(
            ids=[str(i)],  # Use the index as a unique ID for each function
            embeddings=[embedding],  # Pass embedding as a list of lists
            metadatas=[{
                "function": item["function"],
                "description": item["description"],
                "availability": availability_str,  # Store availability as a string
                "declarations": declarations_str,  # Store declarations as a string
                "format": item.get("format", "N/A"),
                "parameters": parameters_str,  # Store parameters as a string
                "returns": returns_str,  # Store returns as a string
                "usage": usage_str,  # Store usage as a string
                "examples": examples_str  # Store examples as a formatted string
            }]
        )
    print("Data successfully stored in ChromaDB!")

# Step 2: Extract function names from generated C++ code using OpenAI API
def extract_function_names_from_cpp():
    """
    This function extracts function names from C++ code using OpenAI API.
    """
    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a technical support agent for testing equipment. Your primary goal is to help users with various test procedures and code generation tasks. Follow the below steps in order step1) Generate the C++ code for the given prompt step2) list all the functions from the above code \n Following are the instructions to be followed for specific range of values \n For Current Range 10 ?A use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [15 ?A] / 75% [7.5 ?A] / 35% [3.5 ?A], For Current Range 100 ?A use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [150 ?A] / 75% [75 ?A] / 35% [35 ?A], For Current Range 1 mA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [1.5 mA] / 75% [750 ?A] / 35% [350 ?A], For Current Range 10 mA use Voltage Range 3.6 V, 10 V, 30 V, 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 150% [15 mA] / 75% [7.5 mA] / 35% [3.5 mA], For Current Range 50 mA use Voltage Range 80 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [65 mA] / 60% [30 mA] / N/A, For Current Range 100 mA use Voltage Range 3.6 V, 10 V, 30 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [130 mA] / 60% [60 mA] / 20% [20 mA], For Current Range 200 mA use Voltage Range 3.6 V, 10 V Current Clamp Levels (% of Full Scale) No Clamp/MID/LOW 130% [260 mA] / 60% [120 mA] / 20% [40 mA].make sure voltage range should not go above 80 V or below -80 V and current rage should not go above 200 mA or go below -200 mA if it is above range return 'voltage or current is beyond permitted range please correct'"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "using APU32 instrument, force all pins to 0V and then Force -199.9 mA to the pin under test ETS and measure the voltage (MV)?"
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

    # Extract the code content from the response
    json_data = response.json()
    code_content = json_data['choices'][0]['message']['content']

    # Use regex to find function names
    # This regex matches function names, assuming they are followed by an open parenthesis '('
    function_names = re.findall(r'\b\w+\s*(?=\()', code_content)    
    return function_names

# Step 3: Search ChromaDB with the extracted function names
def search_functions_in_chromadb(search_query):
    """
    This function searches ChromaDB using the provided search query and returns the formatted output.
    """
    # Get the collection
    collection = client.get_collection("apu32_functions_in_detail")

    # Generate embeddings for the search query
    response = openai.Embedding.create(
        input=search_query,
        engine="ate-test-embedding-ada"
    )
    query_embedding = response['data'][0]['embedding']

    # Perform search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5  # Return top 5 results
    )

    # Format the output to return
    output = ""
    for result in results["metadatas"][0]:
        output += f"Function Name: {result['function']}\n"
        if 'description' in result:
            output += f"Description: {result['description']}\n"
        output += f"Parameters: {result['parameters']}\n"
        output += f"Returns: {result['returns']}\n"
        output += f"Usage: {result['usage']}\n\n"

    return output


# Execution sequence:
store_data_in_chromadb()  # Step 1: Store data in ChromaDB
function_names = extract_function_names_from_cpp()  # Step 2: Extract function names from C++ code
print(function_names)
system_message = search_functions_in_chromadb(function_names)  # Step 3: Search the functions in ChromaDB and print results
print(system_message)
