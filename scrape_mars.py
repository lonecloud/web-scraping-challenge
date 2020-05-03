from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint
import os
import pandas as pd



def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    Mars_data ={}



    browser = init_browser()
    

    #scrape NASA News

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all("div", class_="list_text")
    

    result = results[0]
    title = result.find('div', class_='content_title').a.get_text()
    body = result.find('div', class_='article_teaser_body').get_text()

    #Mars_data[title] = body
    Mars_data["title"] = title
    Mars_data["body"] = body
    
    



    # scrape Mars photo from NASA
    

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(5)

    image_html = browser.html
    image_soup = bs(image_html,"html.parser")

    image_results = image_soup.find_all("div",class_="img")
    image_result = image_results[0]
    

    
    image = f'https://www.jpl.nasa.gov{image_result.img["src"]}'
        #print(image_result.img['src'])
    Mars_data["image_url"] = image
  



    #Mars_weather variable#
    browser = init_browser()
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    time.sleep(5)

    twitter_html = browser.html
    twitter_soup = bs(twitter_html,"html.parser")

    with open("htmltwitter","w") as f:
        f.write(twitter_soup.prettify())

    texts = []
    for each in twitter_soup.find_all("span"):
        texts.append(each.get_text())
    long_texts = [text for text in texts if (len(text)>100 and "InSight sol" in text)]

    mars_weather=long_texts[0]
    Mars_data["Mars_weather"] = mars_weather



    #Mars Facts

    url_mars_facts = "https://space-facts.com/mars/"

    tables = pd.read_html(url_mars_facts)
    df = tables[0]
    df.columns = ["Mars Facts","Data"]
    mars_fact_html_table = df.to_html()
    Mars_data["html_table"] = mars_fact_html_table

    #Mars Hemispheres
    cerberus_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    schiaparelli_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    syrtis_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    valles_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    
    hemisphere_image_urls =[]

    def mars_hemispheres(hemi_url):
        
    
        browser.visit(hemi_url)

        time.sleep(5)

        hemi_html = browser.html
        hemi_soup = bs(hemi_html,"html.parser")

    

        image_results = hemi_soup.find("div",class_="downloads")
        image_url = image_results.find_all("li")[0].a.get("href")
    
        return image_url

    hemisphere_image_urls.append({'title':'Valles Marineris Hemisphere', 'img_url': mars_hemispheres(valles_url)})   
    hemisphere_image_urls.append({'title':'Cerberus Hemisphere', 'img_url': mars_hemispheres(cerberus_url)})
    hemisphere_image_urls.append({'title':'Schiaparelli Hemisphere', 'img_url': mars_hemispheres(schiaparelli_url)})
    hemisphere_image_urls.append({'title':'Syrtis Major Hemisphere', 'img_url': mars_hemispheres(syrtis_url)})

    Mars_data["Hemisphere"] = hemisphere_image_urls


    return Mars_data