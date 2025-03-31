import requests
from datetime import datetime
import os 
from dotenv import load_dotenv

# Import .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

os.chdir(os.path.dirname(__file__))

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {API_KEY}"  
}


json_data = {
    "user": "u185440",
    "fields": "id, vote, vn.title, finished",
    "filters": ["label", "=", 7], 
    "sort": "finished",
    "reverse": True,
    "results": 5,
}


response = requests.post("https://api.vndb.org/kana/ulist", headers=headers, json=json_data)

#listinfo
if response.status_code == 200:
    data = response.json()

    output_folder = "..\\info"
    os.makedirs(output_folder, exist_ok= True)
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"finished_vns_{current_time}.txt"

    with open(os.path.join(output_folder, file_name), "w", encoding="utf-8") as file:
        file.write("Most Recently Finished Visual Novels\n")
        file.write("=" * 40 + "\n")

        for vn in data['results']:
            title = vn['vn']['title']
            finished_date = vn['finished']
            vote = vn.get('vote', 'N/A')
            vn_id = vn['id']
            
            file.write(f"Title: {title}\nFinished On: {finished_date}\nVote: {vote}\nID: {vn_id}\n")
            file.write("-" * 40 + "\n")
    
    print(f"Finished visual novels list has been saved to '{os.path.join(output_folder, file_name)}'.")        
else:
    print(f"Error: {response.status_code}, {response.text}") 
