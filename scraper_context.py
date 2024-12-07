import threading
import random
from typing import List
from selenium import webdriver

class Driver_Container:
    def __init__(self) -> None:
        self.free = False
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

# Thread safe scraper resources
class Scraper_Context:
    def __init__(self, search_term, num_images) -> None:
        self._id = random.randint(1000, 9999)
        self._thread_id = None
        self._thread = None
        self._image_urls: List[int] = []
        self._is_complete = False
        self._search_term = search_term
        self._num_images = num_images
        self._resource_lock = threading.Lock()

    @property
    def id(self) -> int:
        self._resource_lock.acquire()
        ret = self._id
        self._resource_lock.release()
        return ret
    @id.setter
    def id(self, id: int):
        self._resource_lock.acquire()
        self._id = id
        self._resource_lock.release()
    
    @property
    def thread_id(self) -> int:
        self._resource_lock.acquire()
        ret = self._thread.ident
        self._resource_lock.release()
        return ret
    
    @property
    def thread(self) -> threading.Thread:
        self._resource_lock.acquire()
        ret = self._thread
        self._resource_lock.release()
        return ret
    @thread.setter
    def thread(self, thread: threading.Thread):
        self._resource_lock.acquire()
        self._thread = thread
        self._thread_id = thread.ident
        self._resource_lock.release()
    
    @property
    def image_urls(self) -> List[str]:
        self._resource_lock.acquire()
        ret = self._image_urls
        self._resource_lock.release()
        return ret
    @image_urls.setter
    def image_urls(self, image_urls: List[int]):
        self._resource_lock.acquire()
        self._image_urls = image_urls
        self._resource_lock.release()
    def add_image_url(self, image_url: str):
        self._resource_lock.acquire()
        self._image_urls.append(image_url)
        self._resource_lock.release()
    
    @property
    def is_complete(self) -> bool:
        self._resource_lock.acquire()
        ret = self._is_complete
        self._resource_lock.release()
        return ret
    @is_complete.setter
    def is_complete(self, is_complete: bool):
        self._resource_lock.acquire()
        self._is_complete = is_complete
        self._resource_lock.release()
    
    @property
    def search_term(self) -> str:
        self._resource_lock.acquire()
        ret = self._search_term
        self._resource_lock.release()
        return ret
    @search_term.setter
    def search_term(self, search_term: str):
        self._resource_lock.acquire()
        self._search_term = search_term
        self._resource_lock.release()
    
    @property
    def num_images(self) -> int:
        self._resource_lock.acquire()
        ret = self._num_images
        self._resource_lock.release()
        return ret
    @num_images.setter
    def num_images(self, num_images: int):
        self._resource_lock.acquire()
        self._num_images = num_images
        self._resource_lock.release()