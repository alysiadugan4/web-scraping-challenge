from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Setup splinter


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve first title
    titles = soup.find_all('div', class_='content_title')

    news_title = titles[0].get_text() 
   
    paragraphs = soup.find_all('div', class_='article_teaser_body')

    news_para = paragraphs[0].get_text() 

    return news_title, news_para

def featured_img(browser):
  # Navigate to image url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

  # Assign image url to variable
    featured_image_url = ''

    browser.links.find_by_partial_text('FULL IMAGE').click()

    html_img = browser.html
    soup_img = BeautifulSoup(html_img, 'html.parser')

    # Get image source
    mars_image = soup_img.find('img', class_='fancybox-image').get('src')

    featured_image_url = url + mars_image
    return featured_image_url

def mars_facts(browser):
    url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html(url)[1] 
    mars_html_table = mars_facts.to_html()
    
    return mars_html_table

def hemispheres(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Get the links for the hemispheres
    links = browser.links.find_by_partial_text("Hemisphere Enhanced")

    # Setup an empty list
    img_url = []

    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one 
    # dictionary for each hemisphere.

    for link in range(len(links)):
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        browser.links.find_by_partial_text("Hemisphere Enhanced")[link].click()
        
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.find("h2", class_="title")
        title_text = title.text
        img = soup.find("img", class_="wide-image").get("src")
        
        hemisphere_dict = {"Title": title_text, "Img URL": url + img}
        
        img_url.append(hemisphere_dict)
        
        browser.back()

    return img_url