import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Import .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

os.chdir(os.path.dirname(__file__))


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {API_KEY}"
}

#setup
def get_vn_img(vn_id):
    vn_id = str(vn_id)
    
    json_data = {
        "filters": ["id", "=", vn_id],  
        "fields": "id, title, image.url"
    }

    response = requests.post("https://api.vndb.org/kana/vn", headers=headers, json=json_data)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            vn = data["results"][0]
            title = vn["title"]
            img_url = vn.get("image", {}).get("url", None)
            if img_url:
                return title, img_url
    return None

def get_latest_data(folder="..\\info"):
    files = [f for f in os.listdir(folder) if f.startswith("finished_vns_") and f.endswith(".txt")]
    if not files:
        print("No files found.")
        return None 
    return os.path.join(folder, sorted(files, reverse=True)[0]) 

def extract_vns_ids(file_path):
    vn_ids = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("ID:"):
                vn_ids.append(line.strip().split(": ")[1])
    return vn_ids 

def delete_old(vn_ids, img_folder="..\\info\\img"):
    current_img = [f for f in os.listdir(img_folder) if f.endswith(".jpg")]
    valid_file = {f"{vn_id}.jpg" for vn_id in vn_ids}

    for image in current_img: 
        if image not in valid_file:
            try:
                os.remove(os.path.join(img_folder, image))
                print(f"Deleted oldie : {image}")
            except Exception as e:
                print(f"Failed deletion {image}: {e}")  


def save_img(img_url, vn_id, output_folder="..\\info\\img"):
    os.makedirs(output_folder, exist_ok=True)
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(os.path.join(output_folder, f"{vn_id}.jpg"), "wb") as img_file:
            img_file.write(response.content)
    else:
        print(f"Failed to fetch img for VN ID {vn_id}")    

#automation
def fetch_vn_images():
    data_file = get_latest_data()
    if not data_file:
        return 
    
    vn_ids = extract_vns_ids(data_file)
    delete_old(vn_ids)
    
    for vn_id in vn_ids:
        result = get_vn_img(vn_id)
        if result:
            title, img_url = result
            save_img(img_url, vn_id)
        else:
            print(f"No img found for VN ID {vn_id}")    

fetch_vn_images()

 

