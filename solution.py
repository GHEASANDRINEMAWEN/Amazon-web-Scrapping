# A python program that scraps through the website amazon selling book url
# And returns 10 most expensive books with a rating greater than 20000

# Getting the different libraries that will used in this process
import bs4
import requests


# Initialise a variable to store the amazon URL
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

# fetching all the books in the collection
All_books = soup.find_all('li', class_= "zg-item-immersion")

#informing the user to to try again when the programs incurs an edge case
if not len(All_books):
    print("Oops!  Please run the program again. There could be some connection issues or requests is taking so much time")


# Storing books with atleast one rating
Books_having_a_rating = []
for book in All_books:
    if "a-size-small a-link-normal" in str(book):
        # fetching the book_titles, their prices and number of ratings of the have.
        book_title = book.select('#zg-ordered-list li span div span a .p13n-sc-truncate')[0].text
        book_price = book.find('span', class_='p13n-sc-price').text.replace('$', '')
        ratings = book.find('a', class_='a-size-small a-link-normal').text.replace(',', '')
        reviews = book.find('a', class_='a-size-small a-link-normal').text.replace(',', '')
        #initilising a dictionary to store information a book in a collection of books that is a books title, price and ratings
        book_dictionary = {"title": book_title, "rating": int(ratings), 'price': float(book_price)}
        Books_having_a_rating.append(book_dictionary)

# Sorting this books in descending order from highest to lowest with respect to the number of ratings the have.
sorted_books = sorted(Books_having_a_rating, key=lambda d: d['price'], reverse = True)
highest_ratings = []
#getting books with rating greater 20000
for ratings in sorted_books:
    if ratings['rating'] > 20000:
        highest_ratings.append(ratings)

# Getting the top ten most expensive books with respect to the number of ratings
top_10 = highest_ratings[:10]
for book in top_10:
    print(f"{book['title']} has a rating of {book['rating']} and the price is {book['price']}")

