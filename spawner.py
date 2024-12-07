import threading
import scraper_context
import scraper
from typing import List

import scraper
import time

class Scraper_Result:
    def __init__(self, phrase: str, image_urls: List[str]) -> None:
        self.phrase = phrase
        self.image_urls = image_urls
        
        
class Scraper_Spawner:
    def __init__(self, num_images) -> None:
        self.num_images = num_images
        self.drivers = []

    def get_driver(self):
        for container in self.drivers:
            if container.free:
                container.free = False
                return container
        new_container = scraper_context.Driver_Container()
        self.drivers.append(new_container)
        return new_container

    def spawn_thread(self, driver, context):
        self.thread = threading.Thread(
            target = scraper.fetch_images,
            args = (
                driver,
                context,
            ),
            daemon=True)
        
    def calc_timeout_length(self):
        return 30
    
    def run(self, phrases) -> List[Scraper_Result]:
        threads: List[scraper_context.Scraper_Context] = []
        for phrase in phrases:
            driver = self.get_driver()
            context = scraper_context.Scraper_Context(phrase, self.num_images)
            thread = threading.Thread(
                target=scraper.fetch_images,
                args=(driver, context,),
                daemon=True)
            context.thread = thread
            threads.append(context)

        for context in threads:
            #print(context, context.thread)
            context.thread.start()

        count = 0
        timeout = self.calc_timeout_length()
        all_complete = False
        while count < timeout and not all_complete:
            time.sleep(1)
            count += 1
            for context in threads:
                #print(f"context {context.id} complete?", context.is_complete)
                if context.is_complete:
                    all_complete = True
                else:
                    all_complete = False
                    break
        #print("all complete?", all_complete)

        return map(lambda context: Scraper_Result(context.search_term, context.image_urls), threads)




        
