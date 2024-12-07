import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import scraper_context

import inspect

def print_line_number(process_num):
    print("scraper", process_num, "Line number:", inspect.currentframe().f_back.f_lineno)


def fetch_images(driver_container: scraper_context.Driver_Container, context: scraper_context.Scraper_Context):
    returned_files = None
    search_term = context.search_term
    starting_image_index = 1
    num_images = context.num_images
    process_num = context.id
    driver = driver_container.driver
    if not context:
        context = scraper_context.Scraper_Context()
    try:
        #Instantiate chrome driver
        if not driver:
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
            #print("could not find image link")
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
                    #print("could not find image link")
                    raise Exception("could not find image preview link")
                link.click()
                time.sleep(2)
                img = driver.find_element(By.CSS_SELECTOR, "img[jsname=kn3ccd]")
                url =  img.get_attribute("src")
                #print(url)
                #print_line_number(process_num)
                context.add_image_url(url)
            except:
                num_errors += 1
            # try:
            #     #Create an http get request using the image src to save the image file and add file to return array
            #     filename = downloadImage(url, filename)
            #     #returned_files will not have filename if above throws error
            #     returned_files.append(filename)

                
            # except Exception as e:
            #     print(f"error retrieving document {url}")
            #     num_errors += 1
            i += 1
        #print_line_number(process_num)
        context.is_complete = True
        driver_container.free = True

    except Exception as e:
        raise(e)
    finally:
        #print_line_number(process_num)
        pass
    #print_line_number(process_num)
    return returned_files
    

#uncomment to Test
#fetch_images("family teaching", 3, 3)