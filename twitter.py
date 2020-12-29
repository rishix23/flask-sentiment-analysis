from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import pandas
import numpy 
import os
import time
import csv

def create_webdriver_instance():
    print("starting twitter scrap")
    #Initialization method. 
    driver = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())
    driver.chrome_options = webdriver.ChromeOptions()
    driver.chrome_options.add_argument('--headless')
    driver.chrome_options.add_argument('--no-sandbox')
    driver.chrome_options.add_argument('--disable-setuid-sandbox')
    driver.base_url = 'https://twitter.com/search?q='

    save_tweet_data_to_csv(None, 'tweetsFound.csv', 'w')

    get_tweets(driver, "trump")

    print("ending twitter scrap")

    driver.quit()

    # self.chrome_options = webdriver.ChromeOptions()
    # self.chrome_options.add_argument('--headless')
    # self.chrome_options.add_argument('--no-sandbox')
    # self.chrome_options.add_argument('--disable-setuid-sandbox')
    #   you need to provide the path of chromdriver in your system
    # self.browser = webdriver.Chrome(executable_path=os.popen('which chromedriver').read().strip())
    # self.base_url = 'https://twitter.com/search?q='

def get_tweets(driver, query):
    try: 
        driver.get(driver.base_url+query)
        time.sleep(2)
        body = driver.find_element_by_tag_name('body')
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    
        for card in page_cards:
            try:
                tweet = extract_data_from_current_tweet_card(card)
                save_tweet_data_to_csv(tweet, 'tweetsFound.csv')
            except Exception as e: 
                print(e)
        # timeline = self.browser.find_element_by_xpath()
        # timeline = self.browser.find_element_by_id('timeline')
        # tweet_nodes = timeline.find_elements_by_css_selector('tweet')
    except Exception as e: 
        print(e)
    return

def extract_data_from_current_tweet_card(card):
    try:
       user = card.find_element_by_xpath('.//span').text
    except exceptions.NoSuchElementException:
        user = ""
    except exceptions.StaleElementReferenceException:
        return
    try:
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    except exceptions.NoSuchElementException:
        handle = ""
    try:
        """
        If there is no post date here, there it is usually sponsored content, or some
        other form of content where post dates do not apply. You can set a default value
        for the postdate on Exception if you which to keep this record. By default I am
        excluding these.
        """
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except exceptions.NoSuchElementException:
        return
    try:
        _comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    except exceptions.NoSuchElementException:
        _comment = ""
    try:
        _responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    except exceptions.NoSuchElementException:
        _responding = ""
    tweet_text = _comment + _responding
    try:
        reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    except exceptions.NoSuchElementException:
        reply_count = ""
    try:
        retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    except exceptions.NoSuchElementException:
        retweet_count = ""
    try:
        like_count = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    except exceptions.NoSuchElementException:
        like_count = ""
    tweet = (user, handle, postdate, tweet_text, reply_count, retweet_count, like_count)
    return tweet


def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['User', 'Handle', 'PostDate', 'TweetText', 'ReplyCount', 'RetweetCount', 'LikeCount']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)
