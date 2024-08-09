import chromadb
import logging
import json
import logging

logging.basicConfig(level=logging.DEBUG)

# Setup ChromaDB connection
client = chromadb.Client()

# Create or get the collection for users
if "users" not in client.list_collections():
    users = client.create_collection(name="users")
else:
    users = client.get_collection(name="users")


def add_user(phone, user_id, age, gender, occupation, interests):
    # Log the user data that is being stored
    logging.debug(f"Storing user: {phone}, {user_id}, {age}, {gender}, {occupation}, {interests}")
    
    # Store user details along with their selected interests in a dictionary
    user_data = {
        "phone": phone,
        "age": age,
        "gender": gender,
        "occupation": occupation,
        "interests": interests
    }
    
    # Serialize the dictionary to a JSON string
    user_data_str = json.dumps(user_data)
    
    # Store the user data in the collection
    users.add(
        documents=[user_data_str],  # Pass the serialized string
        ids=[str(user_id)]
    )
    
    # Debugging: Print out all stored documents
    all_documents = users.get()
    logging.debug(f"All documents after insertion: {all_documents}")



def get_user(user_id):
    # Attempt to fetch user details by user ID
    logging.debug(f"Attempting to retrieve user with ID: {user_id}")
    
    # Perform the query to retrieve the user by ID
    result = users.get(ids=[str(user_id)])
    
    logging.debug(f"Query result: {result}")
    
    # Check if the result is not empty and contains valid data
    if result and 'documents' in result and len(result['documents']) > 0:
        logging.debug(f"User found: {result['documents'][0]}")
        return result['documents'][0]  # Return the first document
    else:
        logging.debug(f"No user found with ID: {user_id}")
        return None  # Return None if no user is found

