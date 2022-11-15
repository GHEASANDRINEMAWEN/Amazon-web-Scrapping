# A python program that reads
# https://www.amazon.com/gp/bestsellers/books/ref=bsm_nav_pill_print/ref=s9_acss_bw_cg_bsmpill_1c1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-1&pf_rd_r=JSFR919BB1373W4FETRV&pf_rd_t=101&pf_rd_p=65e3ce24-654c-43fb-a17b-86a554348820&pf_rd_i=16857165011
# and gives back an unordered list of the 10 most expensive books
# with at least 20,000 reviews.


# A link to the documentation of the thought process
# https://docs.google.com/document/d/1wyjN5dIoS-EseOdvCFr9gBGbFgrajVyqbgm3-eqDWbU/edit?usp=sharing


import requests
from bs4 import BeautifulSoup

# a variable to store the link to amazon webpage
page_url = 'https://www.amazon.com/Best-Sellers-Books/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 '
                  'Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, /;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate'
}

# using requests.get method to get data from the Amazon website
source = requests.get(page_url, headers=headers)

# using a BeautifulSoup object to represent a parsed object as a whole
soup = BeautifulSoup(source.text, 'lxml')

# storing all items with a li tag that has class = 'zg-item-immersion'
all_books = soup.find_all('li', class_='zg-item-immersion')

# Edge case
if not len(all_books):
    print("The program is taking longer to fetch the data. Please rerun this program")

# a list to store book reviews in general
reviews_collection = []

# Looping through all_books to find reviews of books
for a_book in all_books:
    if 'a-size-small a-link-normal' in str(a_book):
        reviews = a_book.find('a', class_='a-size-small a-link-normal').text.replace(',', '')
        print(reviews)

        # Appending the fetched reviews to the reviews_collection list
        reviews_collection.append(reviews)

# a list to store reviews >= 20000
highest_reviews_collection = []

# Looping through reviews_collections to select those with at least 20000 reviews
for review in reviews_collection:
    if int(review) >= 20000:
        highest_reviews_collection.append(review)

# a list to store the prices corresponding to items in highest_reviews_collection
highest_reviews_collection_prices = []

# Looping through all_books
for a_book in all_books:
    # looping through the collection of those reviews >=2000
    for review in highest_reviews_collection:
        if f"{int(review):,}" in str(a_book):
            for price in a_book.find('span', class_='p13n-sc-price'):
                highest_reviews_collection_prices.append(float(price.replace('$', '')))

# a list to store the top ten prices from prices stored in highest_reviews_collection_prices
top_ten_prices = []

# Looping through a list which stores the prices of the books with at least 20000 reviews
for prices in highest_reviews_collection_prices:
    top_ten_prices.append(prices)

    list_limit = 10

    top_ten_prices.sort()
    top_ten_prices = top_ten_prices[-list_limit:]

# A list to store ten most expensive books with at least 20,000 reviews
ten_popular_books = []

# Looping through all_books
for a_book in all_books:
    # Looping through the collection of highest reviews, those that are greater than or equal to 20000
    for review in highest_reviews_collection:
        if f"{int(review):,}" in str(a_book):
            for price in top_ten_prices:
                if f"${price}" in str(a_book):
                    ten_popular_books.append(a_book.find('div', class_='p13n-sc-truncate').text.strip())

# Printing the 10 popular books
print("An unordered list of the 10 most expensive books with at least 20,000 reviews from AMAZON\n")
n = 1
for book in ten_popular_books:
    print(str(n) + ". " + str(book))
    n += 1