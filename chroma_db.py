# Install the sentence_transformers library
import chromadb
from sentence_transformers import SentenceTransformer  # Import the SentenceTransformer class
import json

# Initialize ChromaDB client and embedding model
client = chromadb.Client()
model = SentenceTransformer('all-mpnet-base-v2')  # Initialize a SentenceTransformer model

# Check if the collection exists and get or create.
collection = client.get_or_create_collection("apu32_functions_in_detail")

# Load JSON data
with open('/content/vectordb_new_data.json', 'r') as f:
    data = json.load(f)

# Iterate over each function, generate embeddings, and store in Chroma DB
for i, item in enumerate(data):  # Use enumerate to get unique IDs for each function
    # Convert the 'description' field to embeddings
    embedding = model.encode(item["description"]).tolist()  # Convert embedding to list

    # Convert the list fields like 'parameters', 'availability', 'examples', etc., into strings
    parameters_str = ', '.join([param["name"] for param in item.get("parameters", [])])
    availability_str = ', '.join(item.get("availability", []))  # Join availability array into a string

    examples = item.get("examples", {})
    if isinstance(examples, dict):
        # Directly access the nested dictionary instead of iterating over items
        # example = examples.get('description', {})  # This line is not needed
        examples_str = f"description: {examples.get('description', 'N/A')}, code: {examples.get('code', 'N/A')}" # Use examples directly here
    else:
        examples_str = "N/A"


    # Check if 'returns' is a dictionary and convert to string
    returns_str = json.dumps(item.get("returns", {})) if isinstance(item.get("returns"), dict) else str(item.get("returns"))

    # Convert any dictionary fields in 'usage' to a JSON string
    usage_str = json.dumps(item.get("usage", {})) if isinstance(item.get("usage"), dict) else str(item.get("usage", "N/A"))

    # Convert other complex fields (like 'declarations') to strings if they are dictionaries
    declarations_str = json.dumps(item.get("declarations", {})) if isinstance(item.get("declarations"), dict) else str(item.get("declarations", "N/A"))

    # Store in Chroma DB with all relevant metadata
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
# You need to re-run the query after adding the descriptions to the metadata
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client and model
client = chromadb.Client()
model = SentenceTransformer('all-mpnet-base-v2')  # You can also use all-mpnet-base-v2 if required

# Get the collection where the data was stored
collection = client.get_collection("apu32_functions_in_detail")

# Define the search query
#search_query = "Measure current on APU-32 pins"
search_query = "list the parameter of lwait()"
# Encode the search query into an embedding
query_embedding = model.encode(search_query).tolist()  # Convert to list

# Perform the search in ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],  # Pass the query embedding
    n_results=5  # Number of top results to return
)

print(results)
# Display search results
# results["metadatas"] is a list of lists, so you need to iterate through the first list then access elements of the inner list.
# Check if 'description' exists in the metadata before accessing it
for result in results["metadatas"][0]:
    #print (result)
    print(f"Function Name: {result['function']}") # Changed 'name' to 'function'
    if 'description' in result:
        print(f"Description: {result['description']}")
    print(f"Parameters: {result['parameters']}")
    print(f"Returns: {result['returns']}")
    print(f"Usage: {result['usage']}")
    print("-" * 50)
