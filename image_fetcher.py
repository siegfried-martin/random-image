import random_phrase
import scraper
import time
from multiprocessing import Process

import argparse
import shutil
import os
import zipfile
from datetime import datetime
import re

import argparse

parser = argparse.ArgumentParser(description='gets google search images based on a random phrase and downloads them to local folder')

parser.add_argument('-n', '--num_images', help='number of images to download per process (default 3)', default="3", type=int)
parser.add_argument('-t', '--times_to_run', help='number of times a new phrase is generated and images are fetched (default 1)', default="1", type=int)
parser.add_argument('-p', '--processes', help='number of concurrent processes for fetching images', default="1", type=int)
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


def fetch_images():
    try:
        wait_time = 20 + (args.processes * 10)
        processes = []
        for i in range(0, args.processes):
            phrase = random_phrase.getRandomPhrase()
            print(phrase)
            p = Process(target=scraper.fetch_images, args = (phrase, 3, args.num_images,))
            p.start()
            processes.append(p)
            open("current_images/"+phrase.replace(" ", "_"), "w")
        time_count = 0
        while time_count < wait_time:
            running = False
            for p in processes:
                if p.is_alive():
                    running = True
            if not running:
                break;
            #print("waiting at time", time_count)
            time_count += 1
            time.sleep(1)
        for p in processes:
            p.kill()

    except Exception as e:
        print("unhandled exception in scraper")
        raise(e)
        return

if __name__ == '__main__':    
    
    if args.force_clean:
        clean_results()
        exit()
    if args.clean:
        clean_results()
    for i in range(0, args.times_to_run):
        fetch_images()



