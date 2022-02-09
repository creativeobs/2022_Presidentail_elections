#pip install ray

#import libraries
from datetime import date, timedelta, datetime
from ig import Instagram
from rappler import Rappler
from twitter import Twitter
import ray
import time
import pandas as pd

#Setting up parameters
driver = 'drivers/msedgedriver.exe'
keyword = 'halalan2022'
keywords = '#halalan2022'
scrolls = 100

#object creation
ig = Instagram(driver, keywords, scrolls)
rap = Rappler(driver, scrolls)
twi = Twitter(keyword, scrolls)

# multiprocessing using ray module
@ray.remote
def rap_func():
    return rap.start()
    
@ray.remote
def twi_func():
    return twi.start()
    
@ray.remote
def ig_func():
    return ig.start()

df_rapr = rap_func.remote()
df_twir = twi_func.remote()
df_igr = ig_func.remote()
df_rap, df_twi, df_ig = ray.get([df_rapr, df_twir, df_igr])

#preprocess dates

sameday = []
today = date.today()
today_ = today.strftime("%d-%m-%Y")

for x in range(24):
    sameday.append(str(x+1) + 'h')
    sameday.append(str(x+1) + ' HOURS AGO')
sameday.append('1 HOUR AGO')
    
def date_ig_parser(x):
    if x in sameday:
        return today_
    elif x.find('d') != -1:
        day = int(x[:x.find('d')])
        return (today - timedelta(days = day)).strftime("%d-%m-%Y") 
    elif x.find('w') != -1:
        day = int(x[:x.find('w')]) * 7
        return (today - timedelta(days = day)).strftime("%d-%m-%Y") 
    
def date_rap_parser(x):
    if x in sameday:
        return today_
    elif x.find(' DAY'):
        return (today - timedelta(days = 1)).strftime("%d-%m-%Y") 
    elif x.find(' DAYS'):
        day = int(x[:x.find(' DAYS')])
        return (today - timedelta(days = day)).strftime("%d-%m-%Y") 
    
def date_twi_parser(x):
    daten = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
    date = daten.strftime("%d-%m-%Y")
    return date

df_rap['Date'] = df_rap['Date'].apply(date_rap_parser)
df_ig['Date'] = df_ig['Date'].apply(date_ig_parser)
df_twi['date'] = df_twi['date'].apply(date_twi_parser)

#preprocess ig post 
df_ig['Post'] = df_ig['Post'].apply(lambda x: ' '.join(x)).apply(lambda x: x.strip("[]'").strip(","))

#combine into a single dataframe
df_rap['source'] = 'Rappler' 
df_twi['source'] = 'Twitter' 
df_ig['source'] = 'Instagram' 


date = list(df_rap['Date']) + list(df_ig['Date']) + list(df_twi['date'])
post = list(df_rap['Title']) + list(df_ig['Post']) + list(df_twi['text'])
source = list(df_rap['source']) + list(df_ig['source']) + list(df_twi['source'])

current_post_df = pd.DataFrame(zip(date,post,source), columns=['Date', 'Post', 'Source'])

try:
    print('Post found ... combining it to the current scraped data')
    saved_post_df = pd.read_csv('outputs/posts.csv')
    final_post_df = saved_post_df.append(current_post_df)
    final_post_df.drop_duplicates(subset=['Post'],inplace=True) 
    
    final_post_df.to_csv('outputs/posts.csv', index=False)
except:
    print('No outputs found! \nCreating new Post csv')
    current_post_df.to_csv('outputs/posts.csv', index=False)
    final_post_df = current_post_df

#process posts

pres_df = pd.read_csv('presidential_candidates.csv', engine='python')

presidents = list(pres_df['NAME'].str.lower())
alias = list(pres_df['ALIAS'].str.lower())


final_posts_daily = list(final_post_df[final_post_df['Date'] == today_]['Post'].str.lower()) #daily
supported_days = [(today-timedelta(x)).strftime("%d-%m-%Y") for x in range(1,9)]
final_posts_weekly = list(final_post_df[final_post_df['Date'].isin(supported_days)]['Post'].str.lower()) #weekly
supported_days = [(today-timedelta(x)).strftime("%d-%m-%Y") for x in range(1,32)]
final_posts_monthly = list(final_post_df[final_post_df['Date'].isin(supported_days)]['Post'].str.lower()) #monthly


def strip_extra_characters(x):
    cleaned = ''
    for c in x:
        if c.isalpha() or c == ' ':
            cleaned += c
    return cleaned

#get the counts
def getcounts(final_posts_param):
    
    pres = {}
    for x in presidents:
        pres[x] = 0
        
    for post in final_posts_param:
        for i, name in enumerate(alias):
            keywords = name.split()
            post_tokens = strip_extra_characters(post).split()
            
            for token in post_tokens:
                if token in keywords:
                    pres[presidents[i]] += 1
                    
    return pres


daily_count_dict = getcounts(final_posts_daily)
weekly_count_dict = getcounts(final_posts_weekly)
monthly_count_dict = getcounts(final_posts_monthly)

daily_count = []      
weekly_count = []    
monthly_count = []    
          
for x in presidents:
    daily_count.append(daily_count_dict[x])
    weekly_count.append(weekly_count_dict[x])
    monthly_count.append(monthly_count_dict[x])
    
data = [today_] + [x for x in daily_count]
presidents = ['Date'] + [strip_extra_characters(x) for x in presidents]

df_counts = pd.DataFrame(data=[data], columns=presidents)
df_counts.to_csv('outputs/presidential_counts.csv', index=False)

time.sleep(3)
print("Webscrape Complete :)")














































