import subprocess
import sys
import os 

#allocation
info_fetcher_script = os.path.join("..\\scripts\\fetch_vndb_data.py")
img_fetcher_script = os.path.join("..\\scripts\\fetch_vndb_image.py")
card_gen_script = os.path.join("..\\scripts\\card_gen.py")

def run_script(script):
    """Runs the script and waits for it to complete"""
    try:
        subprocess.run([sys.executable, script], check=True)
        print(f"{script} ran successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")   

#run
if __name__ == "__main__":
    run_script(info_fetcher_script)   
    run_script(img_fetcher_script)
    run_script(card_gen_script)  