#!/usr/bin/env python
# coding: utf


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time

def scrape_info():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars={}





    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = BeautifulSoup(browser.html,"html.parser")
    results = soup.find_all("div", class_="list_text")
    #result=result.find_all("div", class_="content_title")
    title = []
    paragraph = []

    for result in results:
        title.append(result.find("div", class_="content_title").a.text)
        paragraph.append(result.find("div", class_="article_teaser_body").text)
    #mars["news_title"]=title[0]   
    #mars["news_paragraph"] = paragraph[0]
    newstitle=title[0]
    newsparagraph=paragraph[0]
    mars["news_title"] = newstitle 
    mars["news_paragraph"] = newsparagraph


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id("full_image").click()
    browser.find_link_by_partial_text('more info').click()
    soup = BeautifulSoup(browser.html,"html.parser")
    results = soup.find_all("figure", class_="lede")
    #results.a.img["src"]
    link=results[0].a.img["src"]
    featured_image_url = 'https://www.jpl.nasa.gov' + link
    mars["featured_image"] = featured_image_url





    mars





    # Mars Facts
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    table[0]





    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])





    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars["facts"]=mars_html_table





    # URL of USGS Astrogeology site to be scraped
    # to obtain high resolution images for each of Mar's hemispheres
    usgs_astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_astrogeology_url)

    # Initialize the list for the dictionary of hemisphere images 
    hemisphere_image_urls = []

    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    usgs_astrogeology_html = browser.html
    all_hemisphere_data = BeautifulSoup(usgs_astrogeology_html, 'html.parser')
    #all_hemisphere_data





    hemisphere_results = all_hemisphere_data.find('div', class_='collapsible results').find_all('div',class_='item')
    hemisphere_results





    # Loop through hemisphere results
    for each_hemisphere in hemisphere_results:
        
        # Get each hemisphere title 
        hem_title = each_hemisphere.find('div', class_='description').find('a', class_='itemLink product-item').h3.text
        # Exclude the word 'Enhanced'
        short_hem_title = ' '.join(hem_title.split()[0:-1])
        
        # Get each hemisphere image URL
        base_hem_url = 'https://astrogeology.usgs.gov'

        each_hem_image_url = base_hem_url + each_hemisphere.find('a',class_='itemLink product-item')['href']

        
        browser.visit(each_hem_image_url)
        time.sleep(2)
        each_hem_img_html = browser.html
        each_hem_data = BeautifulSoup(each_hem_img_html, 'html.parser')
        full_image_url = each_hem_data.find('div',class_='downloads').a['href']
        
        each_hemisphere_image = {
            "title" : short_hem_title,
            "image_url" : full_image_url
        }
        print(each_hemisphere_image)
        # Append each hemisphere info to the list of all hemipheres  
        hemisphere_image_urls.append(each_hemisphere_image)
    mars["hemispheres"] = hemisphere_image_urls





    return mars
if __name__=="__main__":
    print(scrape_info())