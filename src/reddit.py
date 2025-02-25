import requests
import random
from io import BytesIO
from pathlib import Path
from PIL import Image
import json

def save_response():
    """Saves the given response dictionary to a JSON file."""
    global response
    filepath = Path(__file__).parent.parent / "response" / "response.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(response, file, indent=4)

# get the saved informations about the last downloaded image 
filepath = Path(__file__).parent.parent / "response" / "response.json"
try:
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as file:
            response=json.load(file)
except:
    print("file is empty or inexistent")

if "response" not in globals():
    response = {"Author":"","Source":""}
    save_response()
print(response)


def downloadimage(url):
    """downloads the image, converts it to a .png and saves it as response/response.png"""
    filepath = Path(__file__).parent.parent / "response" / "response.jpg"
    filepath.parent.mkdir(parents=True, exist_ok=True) # make sure the path exists, if not, create it
    
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")  # converts image to PNG
        
        image.save(filepath, "JPEG", optimize=True)
        print(f"Image downloaded, converted to JPEG, and saved as {filepath}")
    else:
        print("Failed to download image. HTTP Status code:", response.status_code)
  

def reloadimage():
    """Fetches a random image from a subreddit and saves it as response.jpg"""
    global response
    subreddits = ["femboy", "FemboyFashion", "femboymemes","Femboy_Hispanos",
                  "FemboyFitness", "teenfemboy", "femboy_thighs_", "fempark",
                  "GothFemboy", "FemboyStyle", "StraightFemboys", "FemboyNation",
                  "MildFemboys"]
    nsfw_subreddits = ["femboys","FemboyHentai","Femboy4real", "femboycum"] 
    subreddit = random.choice(subreddits)
    subreddit = "wallpapers"

    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"

    print(f'fetching {url}')

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()

        posts = [post["data"] for post in data["data"]["children"] if "url" in post["data"]]
        image_posts = [p for p in posts if p["url"].endswith(("jpg", "png", "jpeg"))]

        if not image_posts:
            return({"errors":"No images found in the subreddit."})

        chosen_post = random.choice(image_posts)
        image_url = chosen_post["url"]
        author = chosen_post["author"]
        source = f"https://www.reddit.com{chosen_post['permalink']}"

        print(f"downloading image from {image_url}")
        downloadimage(image_url)

        response["Author"] = author
        response["Source"] = source
        save_response()

        print(f"Image saved successfully!")
        return True


    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def getresponce():
    """returns the global response varible"""
    global response
    return response

