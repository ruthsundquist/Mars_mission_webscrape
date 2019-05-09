#!/usr/bin/env python
# coding: utf-8
# the Jupyter nb exported as a python file to pass scrape results to Mongo
# In[49]:


# Dependencies
from bs4 import BeautifulSoup as bs # Scraping
import requests as req # Connects to the url
import re #regular expressions
import os
import pandas as pd
from splinter import Browser
import pymongo
from flask import Flask
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MissionMars
def scrape():
    # In[50]:

    NasaMars = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response = req.get(NasaMars) #connect to the site
    html_soup = bs(response.text, 'html.parser') 

    context =  html_soup.find('body').       find('div', {"class":"image_and_description_container"})

    para = context.find("div",{"class":"rollover_description_inner"}).get_text()

    title = (context.find_all('img')[1]).get('alt')

    img = (context.find_all('img')[1]).get('data-lazy')

    print(title)
    print(para)
    print(img)

    # In[51]:



    executable_path = {'executable_path': 'chromedriver_win32/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    response = req.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars') #connect to the site
    html_soup = bs(response.text, 'html.parser') 

    featured_image_url =  html_soup.find('body').       find('article', {"class":"carousel_item"}).get('style').split("'")[1]


    featured_image_url=('https://www.jpl.nasa.gov/'+ featured_image_url)#complete url string 

    browser.visit(featured_image_url)
   

    # In[52]:


    #Mars weather twitter  

    html = "https://twitter.com/marswxreport?lang=en"
    response = req.get("https://twitter.com/marswxreport?lang=en") #connect to the site
    html_soup = bs(response.text, 'html.parser') 

    mars_weather =  html_soup.find('body').       find('div',{"class":"js-tweet-text-container"}).get_text()

    print(mars_weather)


    # In[53]:


    #Mars facts page
    html = "https://space-facts.com/mars/"

    tables = pd.read_html("https://space-facts.com/mars/")[0]
    
    print(type (tables))
    html_table = tables.to_html()
    html_table


    # In[54]:


    #Mars astrogeology site

    mars = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    rep3 = req.get(mars)
    html3 = bs(rep3.text, 'html.parser')
    test = html3.find('body')
        
    links = []

    for i in range(4):
        link = test.select('div.item')[i].find('a')
        links.append(link['href'])
        
        
    for i in links:
        inreq = req.get("https://astrogeology.usgs.gov" + i)
        inreq = req.get("https://astrogeology.usgs.gov" + i)
        rep4 = bs(inreq.text, 'html.parser')
        test2 = rep4.find('div', {"class":"downloads"}).select('a')[1]['href']
        print(test2)
        test3 = rep4.find('div', {"class":"content"}).find('h2').get_text()
        print(test3)

        mars_hemisphere =  rep4.find('body').       find('div',{"class":"downloads"}).select ('a')[1]
    print(mars_hemisphere)


    # In[57]:


    #python dictionary to store data using keys title and img_url



    # In[59]:


    dictlist = [{"title": "Cerberus", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"title":"Schiaparelli", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"title":"Syrtis Major","img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
    {"title":"Valles Marineris", "img_url":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"}]



    # In[60]:


    print(dictlist)
#this dictionary summarized the 5 scraped websites and the values are the input to MOngo db
    dictionary = {"facts": html_table,
                "weather": mars_weather,
                "nasa": {"title":title, "context": para, "photo": img},
                "jpl": featured_image_url,
                "geol": dictlist}

    return(dictionary)

# print(scrape())


# app= Flask(__name__)
# @app.route("/scrape")
# def scrapemongo():
#     return scrape

# if __name__ == "__main__":  
#     app.run(debug=True)







#%%
