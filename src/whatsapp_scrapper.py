"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WhatsappScrapper():
    def __init__(self, page, browser, browser_path):
        self.page = page
        self.browser = browser
        self.browser_path = browser_path
        self.driver = self.load_driver()

        # Open the web page with the given browser
        self.driver.get(self.page)

    def load_driver(self):
        """
        Load the Selenium driver depending on the browser
        (Edge and Safari are not running yet)
        """
        driver = None
        if self.browser == 'firefox':
            firefox_profile = webdriver.FirefoxProfile(
                self.browser_path)
            driver = webdriver.Firefox(firefox_profile)
        elif self.browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            if self.browser_path:
                chrome_options.add_argument('user-data-dir=' +
                                            self.browser_path)
            driver = webdriver.Chrome(options=chrome_options)
        elif self.browser == 'safari':
            pass
        elif self.browser == 'edge':
            pass

        return driver

    def open_conversation(self, name):
        """
        Function that search the specified user by the 'name' and opens the conversation.
        """

        while True:
            for chatter in self.driver.find_elements_by_xpath("//div[@id='pane-side']/div/div/div/div"):
                chatter_path = "//span[contains(@title,'{}')]".format(
                    name)
                try:
                    chatter_name = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, chatter_path))
                    ).text
                except StaleElementReferenceException:
                    chatter_name = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, chatter_path))
                    ).text

                if chatter_name == name:
                    chatter.find_element_by_xpath(
                        ".//div/div").click()
                    return True

    def read_last_in_message(self):
        """
        Reading the last message that you got in from the chatter
        """
        for messages in self.driver.find_elements_by_xpath(
                "//div[contains(@class,'message-in')]"):
            try:
                message = ""
                emojis = []

                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")

                message = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
                ).text

                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))

            except NoSuchElementException:  # In case there are only emojis in the message
                try:
                    message = ""
                    emojis = []
                    message_container = messages.find_element_by_xpath(
                        ".//div[contains(@class,'copyable-text')]")

                    for emoji in message_container.find_elements_by_xpath(
                            ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                    ):
                        emojis.append(emoji.get_attribute("data-plain-text"))
                except NoSuchElementException:
                    pass

        return message, emojis
