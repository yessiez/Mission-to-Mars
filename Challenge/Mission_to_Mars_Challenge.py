#!/usr/bin/env python
# coding: utf-8

# Import dependencies
# Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
# Import Pandas
import pandas as pd


# Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
# Set up the URL for scraping
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# Begin scraping
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL (add base URL)
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts
# Scrape table with Pandas
# Create a new DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# Assign columns to the new Data Frame
df.columns = ['Description', 'Mars', 'Earth']

# Turn the Description column into the DataFrame's index
df.set_index('Description', inplace=True)

# Display DataFrame
df


# Convert DataFrame back into HTML-ready code
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL
url = 'https://marshemispheres.com/'
browser.visit(url)


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# 3. Write code to retrieve the image urls and titles for each hemisphere image.
for i in range(4):
    # create empty dictionary
    hemispheres = {}

    # Click on each hemisphere link
    browser.find_by_css('a.product-item h3')[i].click()

    # Navigate to the full-resolution image page
    element = browser.links.find_by_text('Sample').first

    # Retrieve the full-resolution image URL string and title for the hemisphere image
    img_url = element['href']
    title = browser.find_by_css("h2.title").text

    # Save the full-resolution image URL string
    hemispheres["img_url"] = img_url

    # Save the hemisphere image title
    hemispheres["title"] = title

    # Add img_url and title to hemispheres dictionary
    hemisphere_image_urls.append(hemispheres)

    # Navigate back to the beginning to get the next hemisphere image
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()
