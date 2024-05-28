import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class WebDriverManager:
    def __init__(self, grid_url=None):
        if grid_url:
            self.driver = self.setup_grid_driver(grid_url)
        else:
            self.driver = self.setup_local_driver()

    def setup_grid_driver(self, grid_url):
        ff_options = Options()
        ff_options.add_argument("--headless")
        return webdriver.Remote(
            command_executor=grid_url,
            options=ff_options
        )

    def setup_local_driver(self):
        return webdriver.Firefox()

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

