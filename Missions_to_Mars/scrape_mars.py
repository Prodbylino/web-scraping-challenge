# Import Libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Scrape the Mars data from all the websites
def scrape():
    # Create a results dictionary
    results_dictionary = {}
    
    # Scrape data from the 'Red Planet Science' website
    # Set up the web browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Set the website url
    url = "https://redplanetscience.com/"
    # Visit the website
    browser.visit(url)
    time.sleep(2)
    # Scrape the most recent NASA news (which is a different article every time)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    # Quit the browser
    browser.quit()
    #Add result to results dictionary
    results_dictionary["Most_Recent_News"] = {"title":news_title, "paragraph":news_p}
    
    # Scrape data from the 'Space Images Mars' website
    # Set up the web browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Set the website url
    url = "https://spaceimages-mars.com/"
    # Visit the website
    browser.visit(url)
    time.sleep(2)
    # Scrape the featured image file
    html = browser.html
    soup = bs(html, "html.parser")
    featured_image = soup.find('img', class_='headerimage fade-in')
    # Create the featured image url
    featured_image_url = url + featured_image['src']
    # Quit the browser
    browser.quit()
    #Add result to results dictionary
    results_dictionary['Featured_Image_URL'] = featured_image_url
    
    # Scrape data from the 'Galaxy Facts Mars' website
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    planet_profile_table = tables[0]
    # Rename columns
    planet_profile_table.columns = ['Description','Mars','Earth']
    # Reset index
    planet_profile_table = planet_profile_table.set_index('Description')
    # Convert DataFrame to String
    planet_profile_table_html_string = planet_profile_table.to_html()
    # Clean the string
    planet_profile_table_html_string = planet_profile_table_html_string.replace('\n', '')
    # Add Bootstrap to the table
    planet_profile_table_html_string = planet_profile_table_html_string.replace( "dataframe", "table table-striped" )
    # Change tr style to "text-align: left;"
    planet_profile_table_html_string = planet_profile_table_html_string.replace( "text-align: right;", "text-align: left;" )
    #Add result to results dictionary
    results_dictionary['Planet_Profile_Table_HTML_String'] = planet_profile_table_html_string
    
    # Scrape data from the 'Mars Hemispheres' website
    # Set up the web browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Visit the website
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(2)
    # Scrape the hemisphere data
    html = browser.html
    soup = bs(html, "html.parser")
    hemispheres = soup.find_all('div', class_='item')
    # Quit the browser
    browser.quit()
    # Create the Mars Hemisphere Image Url dictionary list
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        # Get the hemisphere image link
        hemisphere_image_src = hemisphere.find('img', class_='thumb')['src']
         # Create the hemisphere image url
        hemisphere_image_url = url + hemisphere_image_src
        # Get the hemisphere title
        hemisphere_title = hemisphere.find('h3').get_text()
        # Add hemisphere title and image_url to a dictionary and add this to a list
        hemisphere_image_urls.append({'title':hemisphere_title, 'image_url':hemisphere_image_url})
    #Add result to results dictionary
    results_dictionary['Hemisphere_Image_URLs'] = hemisphere_image_urls
    
    # Return the results dictionary
    return results_dictionary