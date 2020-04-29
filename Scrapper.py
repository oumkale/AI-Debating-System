#!/usr/bin/env python
# coding: utf-8

import requests
import numpy as np
import re
import time
import nltk
import pickle
from multiprocessing import Pool
from pprint import pprint
from googlesearch import search
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options




# chrome_options = Options()
# # chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')





# # Query Processing

# ### List of all the websites for the Google Custom Search Engine

websites = {
            'wikipedia' : 'www.wikipedia.com',
            'ndtv' : 'https://www.ndtv.com/',
            'hindustantimes' : 'https://www.hindustantimes.com/',
            'thehindu' : 'https://www.thehindu.com/',
            'theguardian' : 'https://www.theguardian.com/',
            'dailymail' : 'https://www.dailymail.co.uk/home/index.html',
            'news18' : 'https://www.news18.com/',
            'gizmochina' : 'https://www.gizmochina.com/',
            'thewire' : 'https://thewire.in/',
            'bbc' : 'https://www.bbc.com/news/',
            'moneycontrol' : 'https://www.moneycontrol.com/news/',
            'economictimes' : 'https://economictimes.indiatimes.com/',
            'businessinsider' : 'https://www.businessinsider.in/',
            'cnbc' : 'https://www.cnbc.com/',
            'vice' : 'https://www.vice.com/en_us/article/',
            'wired' : 'https://www.wired.com/story/',
            'debate' : 'https://www.debate.org/debates/'        
            }


# ### Google Custom Search Engine


def get_links(query,n):
    if n > 100:
        n = 100
    n = int(n/10)
    from googleapiclient.discovery import build
    service = build("customsearch", "v1",
            developerKey="AIzaSyAaNd94yE8FU5OeRgS6C9o45wZ3geNs4iQ")
    page = 1
    links = []
    for j in range(0,n):
        res = service.cse().list(
              q = query,
              cx='005667722223655693261:hokwdhe2r8y',
              start=page,
            ).execute()
        page += 10
        if 'items' in res.keys():
            for i in res['items']:
                links.append(i['link'])
    return links


# ### Raw Text Scrapping 


articles = []
def get_articles(links):
    # Run this with a pool of 10 agents having a chunksize of 10 until finished
    agents = len(links)//10
    chunksize = 10
    articles = []
    with Pool(processes=agents) as pool:
        articles = pool.map(scrap_articles, links,chunksize)
    return articles


def scrap_articles(link):
    websites = {
            'wikipedia' : 'www.wikipedia.com',
            'ndtv' : 'https://www.ndtv.com/',
            'hindustantimes' : 'https://www.hindustantimes.com/',
            'thehindu' : 'https://www.thehindu.com/',
            'theguardian' : 'https://www.theguardian.com/',
            'dailymail' : 'https://www.dailymail.co.uk/home/index.html',
            'news18' : 'https://www.news18.com/',
            'gizmochina' : 'https://www.gizmochina.com/',
            'thewire' : 'https://thewire.in/',
            'bbc' : 'https://www.bbc.com/news/',
            'moneycontrol' : 'https://www.moneycontrol.com/news/',
            'economictimes' : 'https://economictimes.indiatimes.com/',
            'businessinsider' : 'https://www.businessinsider.in/',
            'cnbc' : 'https://www.cnbc.com/',
            'vice' : 'https://www.vice.com/en_us/article/',
            'wired' : 'https://www.wired.com/story/',
            'debate' : 'https://www.debate.org/debates/'        
            }
    keylist = list(websites.keys())
    print(link)
    if keylist[0] in link:
        raw_text = get_wikipedia_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[1] in link:
        raw_text = get_ndtv_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[2] in link:
        raw_text = get_hindustan_times_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[3] in link:
        raw_text = get_the_hindu_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[4] in link:
        raw_text = get_the_guardian_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[5] in link:
        raw_text = get_daily_mail_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[6] in link:
        raw_text = get_news_18_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[7] in link:
        raw_text = get_gizmochina_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[8] in link:
        raw_text = get_the_wire_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[9] in link:
        raw_text = get_bbcworldnews_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[10] in link:
        raw_text = get_moneycontrol_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[11] in link:
        raw_text = get_economictimes_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[12] in link:
        raw_text = get_businessinsider_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[13] in link:
        raw_text = get_cnbc_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[14] in link:
        raw_text = get_vice_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[15] in link:
        raw_text = get_wired_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    elif keylist[16] in link:
        raw_text = get_debate_org_data(link)
        if(raw_text != 0):
            articles.append(raw_text)
    return raw_text


# # Scrapping Methods

#Wikipedia
def get_wikipedia_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    body = BeautifulSoup(article.text,"lxml")
    if len(body) == 0:
        return 0
    x = body.select('p')
    if len(x) == 0:
        return 0
    raw_text = ''
    for i in range(len(x)):
        raw_text = raw_text + x[i].getText()
    return raw_text

# get_wikipedia_data('https://en.wikipedia.org/wiki/Machine_learning')



def get_the_guardian_data(link):
    if "live" in link:  
        return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='content__article-body from-content-api js-article__body')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text
        




def get_daily_mail_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('p', class_='mol-para-with-font')
    if len(body) == 0:
        return 0
    x = body
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    # Removing special characters
    raw_text = re.sub("\\xa0", "", final_article)
    return raw_text




def get_the_hindu_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='article')
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='article')
    if len(body) == 0:
        return 0
    soup_article = BeautifulSoup(str(body[0]))
    x = soup_article.find_all('p')
    if len(x) == 0:
        return 0
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text





def get_ndtv_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='sp-cn ins_storybody')
    if len(body) == 0:
        return 0
    soup_article = BeautifulSoup(str(body[0]),'html5lib')
    x = soup_article.find_all('p')
    if len(x) == 0:
        return 0
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    raw_text = re.sub("\\xa0", "", raw_text)
    return raw_text




def get_hindustan_times_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='storyDetail')
    if len(body) == 0:
        return 0
    soup_article = BeautifulSoup(str(body[0]),'html5lib')
    x = soup_article.find_all('p')
    if len(x) == 0:
        return 0
    #Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
#     raw_text = re.sub("\\xa0", "", raw_text)
    return raw_text





def get_news_18_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('article', class_='article-content-box')
    if len(body) == 0:
        return 0
    soup_article = BeautifulSoup(str(body[0]),'html5lib')
    x = soup_article.find_all('p')
    if len(x) == 0:
        return 0
    #Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text





def get_gizmochina_data(link):
    if "live" in link:  
        return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='td-post-content')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text
    
# get_gizmochina_data('https://www.gizmochina.com/2020/03/06/south-korea-supply-chain-issues-coronavirus/')




def get_the_wire_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='grey-text')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text

# get_the_wire_data('https://thewire.in/communalism/delhi-riots-aali-village-hindus-muslims')




def get_bbcworldnews_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='story-body__inner')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text
    
# get_bbcworldnews_data('https://www.bbc.com/news/world-us-canada-51762753')




def get_moneycontrol_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='arti-flow')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text

# get_moneycontrol_data('https://www.moneycontrol.com/news/world/samsung-suspends-smartphone-factory-in-south-korea-again-after-new-coronavirus-case-5010091.html')




def get_economictimes_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='Normal')
    if len(body) == 0:
        return 0
    x = body
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text

# get_economictimes_data('https://economictimes.indiatimes.com/industry/banking/finance/banking/yes-bank-withdrawal-limit-capped-at-rs-50000/articleshow/74498382.cms')




def get_businessinsider_data(link):
    if "live" in link:  
        return 0
    article = requests.get(link)
    article.status_code
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='Normal')
    if len(body) == 0:
        return 0
    x = body
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text

# get_businessinsider_data('https://www.businessinsider.in/finance/news/indias-largest-bank-stock-sees-the-sharpest-fall-in-over-7-years-investors-want-to-say-no-to-yes-bank/articleshow/74504449.cms')




def get_cnbc_data(link):
    if "live" in link:  
        return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='ArticleBody-articleBody')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text

# get_cnbc_data('https://www.cnbc.com/2020/03/06/opec-meeting-coronavirus-weighs-on-oil-demand-as-oil-prices-fall.html')




def get_vice_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='article-keep-reading')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    return raw_text
# get_vice_data('https://www.vice.com/en_us/article/884kgv/sanders-v-biden-is-about-to-get-really-really-ugly')




def get_wired_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='article__chunks')
    if len(body) == 0:
        return 0
    x = body[0].find_all('p')
    if len(x) == 0:
        return 0
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    raw_text = re.sub("\\xa0", "", raw_text)
    return raw_text

# get_wired_data('https://www.wired.com/story/opinion-websites-ask-for-permissions-and-attack-forgiveness/')




def get_debate_org_data(link):
    if "live" in link:  
            return 0
    article = requests.get(link)
    article.status_code
    if '200' not in str(article):
        return 0
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_='round-inner')
    if len(body) == 0:
        return 0
    x = body
    if len(x) == 0:
        return 0
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        raw_text = " ".join(list_paragraphs)
    raw_text = re.sub("\\xa0", "", raw_text)
    raw_text = re.sub("Pro\n", "", raw_text)
    raw_text = re.sub("Con\n", "", raw_text)
    return raw_text


# get_debate_org_data('https://www.debate.org/debates/God-isnt-needed-for-the-existence-of-the-universe./1/')


# # Execution

# path = 'Datasets/Articles/'
# topic = 'Abortion'
# links = get_links(topic,100)
# # pprint(links)

# print(len(links))

# articles=get_articles(links)
# save_data(path+topic,articles)