from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class BrowserAutomation:
    def __init__(self):
        self.driver = None

    def _init_driver(self):
        if not self.driver:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True) # Keep browser open
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.maximize_window()

    def search_google(self, query: str):
        """Search google for a specific query."""
        try:
            self._init_driver()
            self.driver.get('https://www.google.com')
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            return True, f"Searched Google for {query}"
        except Exception as e:
            return False, f"Failed to search: {e}"

    def open_website(self, url: str):
        """Open a specific URL."""
        try:
            self._init_driver()
            if not url.startswith('http'):
                url = 'https://' + url
            self.driver.get(url)
            return True, f"Opened {url}"
        except Exception as e:
            return False, f"Failed to open website: {e}"

    def close_browser(self):
        """Close the browser if open."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            return True, "Browser closed"
        return False, "Browser was not open"
