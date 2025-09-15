import requests # type: ignore
import random
from io import BytesIO
from pathlib import Path
from PIL import Image  # type: ignore
import json
import tempfile
import os

from tools import *

def save_response():
    """Saves the given response dictionary to a JSON file."""
    global response
    filepath = Path(tempfile.gettempdir()) / "femboydownloader" / "response.json"
    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(response, file, indent=4)

# get the saved informations about the last downloaded image 
filepath = Path(tempfile.gettempdir()) / "femboydownloader" / "response.json"
try:
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as file:
            response=json.load(file)
except:
    log_error("file is empty or inexistent")

if "response" not in globals():
    response = {"Author":"","Source":""}
    save_response()
log(response)


def downloadimage(url):
    """downloads the image, converts it to a .png and saves it as /tmp/femboydownloader/response.png"""
    filepath = Path(tempfile.gettempdir()) / "femboydownloader" / "response.jpg"
    filepath.parent.mkdir(parents=True, exist_ok=True) # make sure the path exists, if not, create it
    
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")  # converts image to PNG
        
        image.save(filepath, "JPEG", optimize=True)
        log(f"Image downloaded, converted to JPEG, and saved as {filepath}")
    else:
        log_error("Failed to download image. HTTP Status code:", response.status_code)

def get_nsfw_preferences():
    filepath = Path.home() / ".config" / "femboydownloader" / "settings" / "settings.json"
    if os.path.exists(filepath) == False:
        log_error("preferences file doesn't exist,  using default preferences")
        return False
    
    file = str(filepath)
    try:
        f = open(file, 'r')
        preferences = json.loads(f.read())
        f.close()
    except Exception as e:
        log_error(e)
    
    return preferences["nsfw"]

def reloadimage():
    """Fetches a random image from a subreddit and saves it as response.jpg"""
    global response
    subreddits = ["femboy", "FemboyFashion", "femboymemes","Femboy_Hispanos",
                  "FemboyFitness", "teenfemboy", "femboy_thighs_", "fempark",
                  "GothFemboy", "FemboyStyle", "StraightFemboys", "FemboyNation",
                  "MildFemboys"]
    nsfw_subreddits = ["femboys","FemboyHentai","Femboy4real", "femboycum"] 
    if get_nsfw_preferences() == True:
        subreddits += nsfw_subreddits
        
    subreddit = random.choice(subreddits)
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"

    log(f'fetching {url}')

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        try:
            data = res.json()
        except json.JSONDecodeError as e:
            return "Error while decoding JSON", {"errors": f"Error fetching data: {str(e)}"}

        posts = [post["data"] for post in data["data"]["children"] if "url" in post["data"]]
        image_posts = [p for p in posts if p["url"].endswith(("jpg", "png", "jpeg"))]

        if not image_posts:
            return "error while chosing image", {"errors":"No images found in the subreddit."}

        chosen_post = random.choice(image_posts)
        image_url = chosen_post["url"]
        author = chosen_post["author"]
        source = f"https://www.reddit.com{chosen_post['permalink']}"

        log(f"downloading image from {image_url}")
        downloadimage(image_url)

        response["Author"] = author
        response["Source"] = source
        save_response()

        log(f"Image saved successfully!")
        
        return True
    
    except requests.exceptions.RequestException as e:
        return "HTTP error", {"errors": f"Request error: {str(e)}"}
    except Exception as e:
        return "HTTP error", {"errors": f"Unexpected error: {str(e)}"}

def getresponce():
    """returns the global response varible"""
    global response
    return response

