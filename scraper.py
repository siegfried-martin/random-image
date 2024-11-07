import time

from bs4 import BeautifulSoup

import urllib.request
import mimetypes
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from PIL import Image

def is_image_corrupt(image_path):
    try:
        img = Image.open(image_path)
        img.verify()  # Verify the image integrity
        return False  # Image is not corrupt
    except (IOError, SyntaxError) as e:
        return True  # Image is likely corrup


def fetch_images(search_term, starting_image_index=1, num_images=1):
    returned_files = None
    try:
        #Instantiate chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get('http://www.google.com/');

        #perform initial search
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_term)
        search_box.submit()

        #switch to image search
        link = driver.find_element(By.LINK_TEXT, "Images")
        if not link:
            print("could not find image link")
            raise Exception("could not find image link")
        link.click()
        time.sleep(1)
        
        #find all image preview containers using html parser
        container = driver.find_element(By.CSS_SELECTOR, "div[jscontroller=XW992c]")
        if not container:
            raise Exception("could not find image previews")
        html_string = container.get_attribute('innerHTML')
        soup = BeautifulSoup(html_string, "html.parser")
        divs = soup.find_all("div", class_ = "F0uyec")

        #loop through images and clikc to get larger image
        returned_files = []
        i = starting_image_index
        num_errors = 0
        while i < starting_image_index + num_images + num_errors:
            try:
                div = divs[i]
                identifier = div["data-vhid"]
                selector = f'div[data-vhid="{identifier}"]'
                link = driver.find_element(By.CSS_SELECTOR, selector)
            
                if not link:
                    print("could not find image link")
                    raise Exception("could not find image preview link")
                link.click()
                time.sleep(2)
                img = driver.find_element(By.CSS_SELECTOR, "img[jsname=kn3ccd]")
                url =  img.get_attribute("src")
            
                print(url)
                extention = url.split(".")[-1] or "jpg"
                #Create an http get request using the image src to save the image file and add file to return array
                now = datetime.datetime.now()
                formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"current_images/data_{formatted_datetime}.{extention}"
            except:
                num_errors += 1
                continue
            try:
                with open(filename, "w") as new_imagefile:
                    time.sleep(1)
                    urllib.request.urlretrieve(url, filename)
                if is_image_corrupt(filename):
                    print(f"corrupt image {filename}")
                    raise Exception("image corrupt")
                returned_files.append(filename)
            except Exception as e:
                print(f"error retrieving document {url}")
                num_errors += 1
            i += 1

    except Exception as e:
        raise(e)
    finally:
        driver.quit()
    exit()
    return returned_files

#uncomment to Test
#fetch_images("family teaching", 3, 3)