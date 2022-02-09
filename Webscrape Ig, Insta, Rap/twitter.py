import pandas as pd
import requests
import json
import time

consumer_key = "RqAFlGd0AeFQ3Z9tVhbeIwhp0"
consumer_secret = "eBcG6xNrVC8EQgghgbQjDS49iOwo3zjd8uxUUG8Jinyc5qi9Nm"
access_token = "4122306912-p2VwXlZujTxlKRmLp4HP7RtS0IdBUppybJLziFb"
access_token_secret = "DiTo1dZP4th63agoLKfydY17JRpXhlthOoi1xtw0dcpK9"
bearer_token ="Bearer AAAAAAAAAAAAAAAAAAAAAIflUQEAAAAAh3h2cIKNaUUN6kmawsj%2B4dcFioE%3DTQdstLlITebsbvNjAwTZyPWdc1h1jB7oNFZPc8ZUKga697ytds"

class Twitter:
    count = 1
    ls_date = []
    ls_text = []
    ls_retweet_count = []
    ls_reply_count = []
    ls_like_count = []
    ls_quote_count = []
    
    def pol_scraper(self, query, bearer_token, size):
        # Initial request
        URL = "https://api.twitter.com/2/tweets/search/recent?query={}%20-is%3Aretweet&tweet.fields=created_at,public_metrics".format(query)
        HEADER = {'Authorization': bearer_token}
        response = requests.get(url = URL, headers = HEADER)
        response_dict = json.loads(response.text)
        next_token = response_dict['meta']['next_token']
         
        self.data_loop(response_dict)
        
         # loop through pagination of request
        for x in range(size-1):
            URL = "https://api.twitter.com/2/tweets/search/recent?next_token={}&query={}%20-is%3Aretweet&tweet.fields=created_at,public_metrics".format(next_token, query)
            response = requests.get(url = URL, headers = HEADER)
            response_dict = json.loads(response.text)
            next_token = response_dict['meta']['next_token']
            
            self.data_loop(response_dict)
        
        df = pd.DataFrame(data={'date':self.ls_date, 
                                'text':self.ls_text, 
                                'retweet':self.ls_retweet_count,
                                'like':self.ls_like_count,
                                'reply':self.ls_reply_count,
                                'qoute':self.ls_quote_count,
                               })
        
        return df
    
    
    def data_loop(self, response_dict):
        global count, ls_date, ls_text
        for i in range(10):
            try:
                print(response_dict['data'][i]['created_at'])
                print(response_dict['data'][i]['text'])
                print(response_dict['data'][i]['public_metrics'])
                print('----------------------------', self.count,'----------------------------')
            
                self.ls_date.append(response_dict['data'][i]['created_at'])
                self.ls_text.append(response_dict['data'][i]['text'])
                self.ls_retweet_count.append(response_dict['data'][i]['public_metrics']['retweet_count'])
                self.ls_reply_count.append(response_dict['data'][i]['public_metrics']['reply_count'])
                self.ls_like_count.append(response_dict['data'][i]['public_metrics']['like_count'])
                self.ls_quote_count.append(response_dict['data'][i]['public_metrics']['quote_count'])
                
                self.count += 1
            except IndexError:
                print('IndexError! Sleeping 5s...')
                time.sleep(5)
                break
                  
            if self.count%1000 == 0:
                print('RateLimit! Sleeping 15min...')
                time.sleep(903)
                
    def __init__(self, keyword, scrolls):
        self.keyword = keyword
        self.scrolls = scrolls
    
    def start(self):
        df = self.pol_scraper(self.keyword, bearer_token, self.scrolls)
        return df