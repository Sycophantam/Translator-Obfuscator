import random
import urllib.parse
import urllib.request
from time import sleep

import requests
from langdetect import DetectorFactory, detect
from selenium import webdriver

DetectorFactory.seed = 0


class Translator:

    def __init__(self):
        self.session = requests.session()
        self.source_URL = 'https://translate.google.com/#view=home&op=translate&sl='
        self.source_lang = 'en'
        # Python has a language detection module that does not recognize as many languages
        # as google translate provides. The languages that the text can be translated into
        # are languages recognized by this language detection module and that are also used in
        # google translate. This also helps make the translation smoother, as google translate
        # supports languages that may not have as expansive of a vocabulary that other languages do,
        # making the translation too different from the original to be entertaining
        self.lang_list = ['pa', 'lv', 'ja', 'sv', 'tr', 'cs', 'cy', 'kn', 'ko', 'pl', 'ru', 'sq', 'ur', 'hr', 'th', 'sk', 'es', 'pt', 'so', 'sl', 'sw', 'ro', 'mk', 'da', 'ca', 'vi', 'bg', 'bn', 'de', 'hu', 'it', 'hi', 'mr', 'ta', 'nl', 'id', 'ne', 'et', 'tl', 'gu', 'fi', 'uk', 'af', 'ar', 'no', 'fa', 'ml', 'lt', 'en', 'te', 'fr', 'el']
        self.tl = self.choose_language()

        # In order for google translate to correctly translate the text, we want to sleep for
        # a short amount of time to allow the webpage to load correctly. .5 seconds is usually good enough
        # for <500 words.
        self.sleep_time = .5

        # Making sure that the program doesn't create a bunch of google tabs when it runs
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    # Chooses a random language from the list and returns it
    def choose_language(self):
        return random.choice(self.lang_list)

    """
    translate
        This function puts text through google translate iterations times
        :param text: String-Text to translate
        :return: String-Translated text
    """
    def translate(self, text, iterations):

        for i in range(iterations):
            urltext = urllib.parse.quote(text)
            url = self.source_URL + self.source_lang + '&tl=' + self.tl + '&text=' + urltext
            self.driver.get(url)

            # We want to sleep for a second to allow for all the web traffic to be updated correctly
            sleep(self.sleep_time)
            xpath = "//span[@class='tlid-translation translation']"
            failed = False
            try:
                text = self.driver.find_element_by_xpath(xpath).text
            except Exception:
                print("Translation failed. Going again")
                i -= 1
                self.sleep_time += .2
                failed = True

            # Setting the source language as the one the text was just translated to and
            # choosing a random new language
            self.source_lang = self.tl

            temp_tl = self.choose_language()
            while temp_tl == self.tl:
                temp_tl = self.choose_language()
            self.tl = temp_tl
            if not failed:
                print("Finished iteration:", i + 1)
        return self.back_to_english(text)

    """
    back_to_english
        This function changes the text from the last iteration of translate()
        back into English
        :param text
            text-Text in another language that gets sent back to English
        :return Text back in English
    """
    def back_to_english(self, text):
        self.tl = 'en'
        url_text = urllib.parse.quote(text)
        url = self.source_URL + self.source_lang + '&tl=' + self.tl + '&text=' + url_text
        self.driver.get(url)
        sleep(self.sleep_time)
        text = self.get_text()

        # Sometimes the code above doesn't work correctly, so if the language
        # is not in English at the end of this, we tell Google to auto detect the language
        # and translate it to English
        count = 0
        while detect(text) != 'en':
            if count > 10:
                print("Translation failed")
                break
            print("Not English")
            url_text = urllib.parse.quote(text)
            url = self.source_URL + 'auto&tl=en&text=' + url_text
            self.driver.get(url)
            sleep(self.sleep_time)
            count += 1
        return self.get_text()

    """
    function get_text
        This function just grabs the 
    """
    def get_text(self):
        xpath = "//span[@class='tlid-translation translation']"
        return self.driver.find_element_by_xpath(xpath).text
