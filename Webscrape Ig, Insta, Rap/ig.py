from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class Instagram:
    
    def __init__(self, webdriverpath, keyword, scrolls):
        self.webdriverpath = webdriverpath
        self.keyword = keyword
        self.scrolls = scrolls
    
    def start(self):
        self.driver = webdriver.Edge(self.webdriverpath)
        self.driver.get("http://www.instagram.com")
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        username.clear()
        username.send_keys("dummytest32") #paste your username in ig here
        password.clear()
        password.send_keys("dummy32") #paste your password in ig here

        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        time.sleep(2)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

        searchbox = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        searchbox.clear()

        searchbox.send_keys(self.keyword)

        time.sleep(2) 
        my_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + self.keyword[1:] + "/')]")))
        my_link.click()


        for i in range(self.scrolls):
            try:
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight)-100);")
                print(f'scroll: {i}')
            except:
                break
        
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        anchors = self.driver.find_elements_by_tag_name('a')
        anchors = [a.get_attribute('href') for a in anchors]

        anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]

        caps = []
        likes = []
        count = 1 
        length = len(anchors)
        for a in anchors:  
            self.driver.get(a)
            time.sleep(1)
            try:
                msg = self.driver.find_element_by_class_name('C4VMK').text
                like = self.driver.find_element_by_class_name('eo2As  ').text.split(' ')[0]
                caps.append(msg)
                likes.append(like)
            except:
                print('no c4vmk tag')
            print(f'progress: {count}/{length}')
            count += 1
        caps

        users = []
        dates = []
        posts = []

        for cap in caps: 
            var = cap.split('\n')
            users.append(var[0])
            posts.append(var[1:-1])
            dates.append(var[-1])

        dat = zip(users, dates, posts, likes)

        df = pd.DataFrame(data= dat, columns=['User', 'Date', 'Post', 'likes'])

        return df