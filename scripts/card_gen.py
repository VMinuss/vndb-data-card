import os
from mako.template import Template
from dotenv import load_dotenv

# Import .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
IMG_DIR = "..\\info\\img\\"

info_folder = "..\\info"
image_folder = os.path.join(info_folder, "img")
os.chdir(os.path.dirname(__file__))

#finding latest file
txt_files = [f for f in os.listdir(info_folder) if f.endswith('.txt')]
if not txt_files:
    print("No .txt file found in info")
    exit()

latest_file = max(txt_files, key=lambda f: os.path.getmtime(os.path.join(info_folder, f)))
latest_file_path = os.path.join(info_folder, latest_file)

print(f"Processed {latest_file}")

#html read and data set
with open("..\\static\\index.html", "r", encoding="utf-8") as f:
    template_content = f.read()

template_content = template_content.replace('href="styles.css"', 'href="../static/styles.css"')

template = Template(template_content)

visual_novels = []

#img recog
image_files = {f.split('.')[0]: f for f in os.listdir(image_folder) if f.endswith('.jpg')}

with open(latest_file_path, "r", encoding="utf-8") as file:
    vn_data = {}

    for line in file:
        if line.startswith('ID:'):
            vn_data['id'] = line.split(':')[1].strip()
        elif line.startswith('Title:'):
            vn_data['title'] = line.split(':')[1].strip()
        elif line.startswith('Vote:'):
            vn_data['vote'] = line.split(':')[1].strip()

        if 'id' in vn_data and 'title' in vn_data and 'vote' in vn_data:
            vn_id = vn_data['id']
            image_file = image_files.get(vn_id)

            if image_file:
                vn_data['image'] = f"{IMG_DIR.replace('\\', '/')}{image_file}"
                visual_novels.append(vn_data)
            else:
                print(f"No image found for ID: {vn_id}")

            vn_data = {}

print("Final visual novels list:", visual_novels)

#html work
html_output = template.render(visual_novels=visual_novels)

output_path = "..\\output\\card.html"
os.makedirs("..\\output", exist_ok=True)

if os.path.exists(output_path):
    os.remove(output_path)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)
        

print(f"Convert success, saved to {output_path}")


