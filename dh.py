## A python program that scraps through the website
# https://www.amazon.com/gp/bestsellers/books/ref=bsm_nav_pill_print/ref=s9_acss_bw_cg_bsmpill_1c1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-1&pf_rd_r=JSFR919BB1373W4FETRV&pf_rd_t=101&pf_rd_p=65e3ce24-654c-43fb-a17b-86a554348820&pf_rd_i=16857165011
# and returns 10 most expensive books

#getting the different libraries that will used in this process
import bs4
import requests



page_url = "https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg=1"
print('please wait, getting the data from the amazon page...')
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 '
                          'Safari/537.36',
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate"
        }

#fetching URL and returning the html to the variable reponse
response = requests.get(page_url, headers=headers, params={'wait': 2})

# using a BeautifulSoup object to represent a parsed object as a whole
soup = bs4.BeautifulSoup(response.text, 'lxml')

# storing all items with a li tag that has class = 'zg-item-immersion'
All_books = soup.find_all('li', class_= "zg-item-immersion")


if not len(All_books):
    print("Oops!  Please run the program again. There could be some connection issues or requests is taking so much time")


Books_having_a_rating = []

for book in All_books:
    if "a-size-small a-link-normal" in str(book):
        # modifying the url to make sure its readible.
        book_title = book.select('#zg-ordered-list li span div span a .p13n-sc-truncate')[0].text
        book_price = book.find('span', class_='p13n-sc-price').text.replace('$', '')
        ratings = book.find('a', class_='a-size-small a-link-normal').text.replace(',', '')
        book_dictionary = {"title": book_title, "rating": int(ratings), 'price': float(book_price)}
        Books_having_a_rating.append(book_dictionary)
        # Books_having_a_rating.append(ratings)
        # Books_having_a_rating.append(book_title)
        # print(type(ratings))

sorted_books = sorted(Books_having_a_rating, key=lambda d: d['price'], reverse = True)
higest_ratings = []
for ratings in sorted_books:
    if ratings['rating'] > 20000:
        higest_ratings.append(ratings)

top_10 = higest_ratings[:10]
for book in top_10:
    print(f"{book['title']} has a rating of {book['rating']} and the price is {book['price']}")