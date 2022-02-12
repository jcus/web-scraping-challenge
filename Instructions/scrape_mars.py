# Use MongoDB with Flask templating to create a new HTML page that displays all of the information 
# that was scraped from the URLs list

# import dependencies
# pip install pymongo
from bs4 import BeautifulSoup as soup
import requests
import pymongo

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
# connect PyMongo driver for MongoDB Python and dependencies
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# containing all of the scraped data.
# Store the return value in Mongo as a Python dictionary

# use scrape all function --Scrape Multiple Pages of a Website
def scrape_all():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # collect information from news page
    news_title, news_paragraph = scrape_news(browser)
    # build the dictionary using the information from the scrapes
    mars_data = {
        "NewsTitle": news_title,
        "NewsParagraph": news_paragraph,
        "FeaturedImage": scrape_feature_img(browser),
        "Facts": scrape_facts_page(browser),
        "Hemispheres": scrape_hemispheres_page(browser),
        "LastUpdated": dt.datetime.now()
    }
    # stop the webdriver
    browser.quit()
    # display output
    return mars_data

# scrape the mars news page
def scrape_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    # set delay for loading the page-- wait_time
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    
    # retrieve the title
    news_title = news_soup.find('div', class_='content_title').text
    # retrieve the paragraph from the headline
    news_p = news_soup.find('div', class_='article_teaser_body').text


    # return the title and paragraph information
    return news_title, news_p

# scrape the featured image page
def scrape_feature_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    featured_image_url = browser.find_by_tag('button')[1]
    featured_image_url.click()


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    image_soup = soup(html, 'html.parser')


    # find the image url
    img_url_rel = image_soup.find('img', class_='fancybox-image').get('src')


    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    # return the image url
    return img_url

# scrap through the facts page
def scrape_facts_page(browser):
    # Visit URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    fact_soup = soup(html, 'html.parser')

    # find the facts location
    facts_location = fact_soup.find('div', class_="diagram mt-4")
    fact_table = facts_location.find('table')

    # create an empty string
    facts = ""

    # add the text to the empty string then return
    facts += str(fact_table)
    return facts

# scrape through the hemispheres pages
def scrape_hemispheres_page(browser):
    # base url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    # Create a list to hold the images and titles
    hemisphere_image_urls = []
    
    # set up the loop to loop through each page
    for i in range(4):
        # hemisphere info dictionary
        hemisphere_info = {}
    
        # find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # find the Sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphere_info["img_url"] = sample['href']
    
        # Get Hemisphere title
        hemisphere_info['title'] = browser.find_by_css('h2.title').text
    
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere_info)
    
        # Finally, we navigate backwards
        browser.back()


    # return the hemisphere url with the titles
    return hemisphere_image_urls



