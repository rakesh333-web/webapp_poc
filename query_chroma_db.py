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