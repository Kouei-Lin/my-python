from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class WebDriverManager:
    def __init__(self, grid_url="http://127.0.0.1:4444/wd/hub"):
        ff_options = Options()
        ff_options.add_argument("--headless")
        self.driver = webdriver.Remote(
            command_executor=grid_url,
            options=ff_options
        )

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()

