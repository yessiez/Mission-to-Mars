# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment/Setup Splinter
    # Set executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # Set up the URL for scraping
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph, = mars_news(browser)

    #hemisphere_image_urls = mars_images(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        # "img_url": imgage_url,
        # "img_title": image_title,
        "hemispheres": mars_images(browser),
        "last_modified": dt.datetime.now(),
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up the HTML parser
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image


def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


# ## Mars Facts
def mars_facts():
    # Scrape table with Pandas
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns to the new Data Frame
    df.columns = ['Description', 'Mars', 'Earth']
    # Turn the Description column into the DataFrame's index
    df.set_index('Description', inplace=True)

    # Convert DataFrame back into HTML-ready code, add bootstrap
    return df.to_html(classes="table table_striped")

    print("You guys rock!!!")


def mars_images(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #items = img_soup.find_all("div", class_="item")

    for i in range(4):
        # create empty dictionary
        hemispheres = {}

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Click on each hemisphere link
        browser.find_by_css('a.product-item h3')[i].click()

        # Navigate to the full-resolution image page
        element = browser.links.find_by_text('Sample').first

        # Retrieve the full-resolution image URL string and title for the hemisphere image
        img_url = element['href']
        img_title = browser.find_by_css("h2.title").text

        # Save the full-resolution image URL string
        hemispheres["img_url"] = img_url
        # Save the hemisphere image title
        hemispheres["img_title"] = img_title

        # Add img_url and title to hemispheres dictionary
        hemisphere_image_urls.append(hemispheres)

        # Navigate back to the beginning to get the next hemisphere image
        browser.back()

    # print(hemisphere_image_urls)

    # return img_url, img_title
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
