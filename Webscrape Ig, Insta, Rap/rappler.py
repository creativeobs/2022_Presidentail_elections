from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import requests
import time
import pandas as pd

class Rappler:
    
    def __init__(self, webdriverpath, scrolls):
        self.webdriverpath = webdriverpath
        self.scrolls = scrolls

    
    def start(self):
        driver = webdriver.Edge(self.webdriverpath)
        url = 'https://www.rappler.com/2022-philippine-elections'
    
        driver.get(url)
        driver.maximize_window()
    
        #loading all website content
        length = self.scrolls
        i = 0;
        element = driver.find_element(By.XPATH, '//button[contains(text(), "Load More")]')
        time.sleep(3)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "ALLOW")]'))).click()
        while 1:
        #for i in range(5):
            if i == self.scrolls:
                break
            try:
                i += 1;
                time.sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(2)
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Load More")]'))).click()
                print(f'Iteration: {i}/{length}')
            except:
                break
    
        time.sleep(5)
    
        #getting news title and upload date
        news = driver.find_elements_by_tag_name('h3')
        dates = driver.find_elements_by_tag_name('time')
        title = []
        times = []
        for new, date in zip(news, dates):
            title.append(new.text)
            times.append(date.text)
    
        #getting link/href for each news
        anchors = driver.find_elements_by_tag_name('a')
        links = []
        i = 0
        for anchor in anchors:
            try:
                if anchor.text == title[i]:
                    links.append(anchor.get_attribute('href'))
                    i += 1
            except:
                break
    
        #getting author
        authors = []
        for link in links:
            html_text = requests.get(link).text
            auth = BeautifulSoup(html_text, 'lxml')
            # authors.append(driver.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 jZXTrG')).text
    
            try:
                try:
                    author = auth.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 bTrYxg').text
                except:
                    author = auth.find('a', class_='A-sc-120nwt8-1 ListAuthor__ListAuthors-sc-15js12l-1 jZXTrG').text
            except:
                author = 'Not Available'
            authors.append(author)
    
        #dataframe to csv file
        
        rap = pd.DataFrame(zip(title, times, authors, links), columns=["Title", "Date", "Publisher", "Website"])
        return rap
