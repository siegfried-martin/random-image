import random_phrase
import spawner
import urllib.request
from PIL import Image


import argparse
import shutil
import os
import zipfile
from datetime import datetime
import re
import random

import argparse

parser = argparse.ArgumentParser(description='gets google search images based on a random phrase and downloads them to local folder')

parser.add_argument('-n', '--num_images', help='number of images to download per process (default 3)', default="3", type=int)
parser.add_argument('-t', '--times_to_run', help='number of times a new phrase is generated and images are fetched (default 1)', default="1", type=int)
parser.add_argument('-p', '--processes', help='number of concurrent processes for fetching images (default 1)', default="1", type=int)
parser.add_argument('-c', '--clean', help='purge existing files to archive', action='store_true')
parser.add_argument('-C', '--force_clean', help='purge existing files to archive and exit application', action='store_true')


args = parser.parse_args()

def clean_results():
    source_dir = 'current_images'
    target_dir = 'archive_images'
        
    file_names = os.listdir(source_dir)
    if not len(file_names):
        return
    
    archive_file = f"{re.sub("( |-|:)","_",str(datetime.now()))}.zip"
    with zipfile.ZipFile(archive_file, "w") as zip_file:
        for file_name in file_names:
            zip_file.write(os.path.join(source_dir, file_name))
            os.remove(os.path.join(source_dir, file_name))
    shutil.move(archive_file, target_dir)

def move_new_images(files):
    target_dir = 'current_images'
        
    for file_name in files:
        try:
            shutil.move(file_name, target_dir)
        except:
            pass

import inspect

def print_line_number():
    print("image_fetcher", "Line number:", inspect.currentframe().f_back.f_lineno)

def downloadImage(url):
    url_no_query = url.split("?")[0]
    extention = url_no_query.split(".")[-1] or "jpg"
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"current_images/_data_{formatted_datetime}-{random.randint(1000, 9999)}.{extention}"
    with open(filename, "w") as new_imagefile:
        try: 
            urllib.request.urlretrieve(url, filename)
        except Exception as e:
            print("failed first time grabbing doc", e)
            urllib.request.urlretrieve(url, filename)
    if is_image_corrupt(filename):
        print(f"corrupt image {filename}")
        raise Exception("image corrupt")
    return filename

def is_image_corrupt(image_path):
    try:
        img = Image.open(image_path)
        img.verify()  # Verify the image integrity
        return False  # Image is not corrupt
    except (IOError, SyntaxError) as e:
        return True  # Image is likely corrupt


def fetch_images():
    driver = spawner.Scraper_Spawner(args.num_images)
    for i in range(0, args.times_to_run):
        phrases = []
        for j in range(0, args.processes):
            phrases.append(random_phrase.getRandomPhrase())
        results = driver.run(phrases)
        for result in results:
            image_downloads = []
            for url in result.image_urls:
                try:
                    image_downloads.append([downloadImage(url), url])
                except Exception as e:
                    print("error downloading file", url, e)
                    #raise e
            if len(image_downloads):
                filename = f"current_images/{result.phrase}.txt"
                file_contents = "\n".join(" | ".join(a) for a in image_downloads)
                f = open(filename, "w")
                f.write(file_contents)
                f.close()

if __name__ == '__main__':    
    
    if args.force_clean:
        clean_results()
        exit()
    if args.clean:
        clean_results()
    fetch_images()
    print_line_number()
    exit()
    print("active threads", threading.enumerate())



