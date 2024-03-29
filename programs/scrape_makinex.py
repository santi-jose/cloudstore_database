from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import shutil

# look for products being sold on Makinex for $x or less
# identify:
# - Product Name
# - Manufacturer
# - Price
# - Link to Product Listing
# - Product category
# - Image Link

def makinex_products_df():
    print('Enter a price ceiling for the products')
    price_ceiling = float(input('>'))
    (print(f'Filtering prices <= {price_ceiling}'))

    # get the html text
    url = 'https://makinex.com/products/'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    html_text = requests.get(url, headers=headers).text

    # get the products
    soup = BeautifulSoup(html_text, 'html.parser')
    products = soup.find_all('div', class_='wpb_column vc_column_container vc_col-sm-6')

    # lists to store data
    names = []
    prices = []
    manufacturers = []
    links = []
    categories = []
    images = []
    time = []

    # loop through products
    for product in products:
        
        # check for products w/ price <= price_ceiling
        price = product.find('h6').text
        price_str = price[1:len(price)].translate({ord('$'): None, ord(','): None})
        price_float = float(price_str) #store price as int
        
        if price_float <= price_ceiling:
            name = product.find('h3').text
            name = name.replace('\n',' ') # replace \n with space ' '
            link = product.find('a')['href']

            # getting image link and category
            image = product.find('img')
            imageLink = image.attrs['src']

            productPage = requests.get(link, headers=headers).text
            soup = BeautifulSoup(productPage, "html.parser")
            try:
                category = soup.find('span', class_="posted_in").text.strip('Category:')
            except:
                category = 'none'

            # getting time of scrape
            dt = datetime.now()

            names.append(name)
            prices.append(price)
            manufacturers.append('Makinex')
            links.append(link)
            images.append(imageLink)
            categories.append(category)
            time.append(dt)

    data = {'Product Name': names, 'Price': prices, 'Manufacturer': manufacturers,'More Info': links, 'Image Link': images, 'Category': categories, 'Time': time}
    df = pd.DataFrame(data)
    #print(df)
    return df

#saving product image 
def get_image(productName, imageLink, headers):
    image = requests.get(imageLink, headers=headers, stream=True)
    if image.status_code == 200:
        with open("/path/to/image/{}.jpg".format(productName), 'wb') as f:
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, f)
