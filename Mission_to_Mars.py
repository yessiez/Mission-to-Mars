# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
# Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
# Set up the URL for scraping
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser
# Convert the browser html to a soup object
html = browser.html
news_soup = soup(html, 'html.parser')

# Parent element
slide_elem = news_soup.select_one('div.list_text')
slide_elem

# Begin scraping
slide_elem.find('div', class_='content_title')


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ## JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL (add base URL)
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts

# Scrape table with Pandas

# Create a new DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Assign columns to the new Data Frame
df.columns = ['description', 'Mars', 'Earth']

# Turn the Description column into the DataFrame's index
df.set_index('description', inplace=True)

# Display DataFrame
df

# Convert DataFrame back into HTML-ready code
df.to_html()

browser.quit()
