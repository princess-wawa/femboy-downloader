import json
from pathlib import Path

# Filepath to store the response

def save_response():
    """Saves the given response dictionary to a JSON file."""
    global response
    filepath = Path(__file__).parent / "response" / "response.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(response, file, indent=4)

def load_response():
    """Loads and returns the response dictionary from the JSON file."""
    global response
    filepath = Path(__file__).parent / "response" / "response.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as file:
            response=json.load(file)

# Example usage
response_data = {"status": "success", "message": "Data saved"}
save_response(response_data)

loaded_data = load_response()
print(loaded_data)  # Output: {'status': 'success', 'message': 'Data saved'}
