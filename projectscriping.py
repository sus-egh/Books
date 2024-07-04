#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

#_____________________pd.series
books_category=pd.Series() #the titles of all the books and its categories
all_books = pd.Series()  #all the books and its prices, categories and ratings
category_mean_price = pd.Series() #the titles of all the books and its avarage values of its prices 
books_rating = pd.Series() #the titles of all the books and its ratings

#______________________Scraping
for page in range(1,51): 
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    url2 = 'https://books.toscrape.com/catalogue/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('h3') # url of each book

 #____________________scraping for each page   
    for b in books:
        b_url = b.find('a')['href']
        b_response = requests.get(url2+b_url)
        b_soup = BeautifulSoup(b_response.content, 'html.parser')

        title = b_soup.find('h1').text #title of the book
        price = b_soup.find('p', class_='price_color').text #price of the book
        category = b_soup.find('ul', class_='breadcrumb').find_all('a')[2].text #category of the book
        rating =  b_soup.find('p', class_='star-rating')['class'][1] #rating of the book

        all_books[title] = float(price[1:]), category, rating #pd serie which keys are  titles and 3 values are price, category and rating
    #book_category
        if category not in books_category.index: #if category doesn't exist in books_category, add it
            books_category[category] = 1
        else: #if exists then +1
            books_category[category]+=1
    #category_mean_price
        if category not in category_mean_price.index: #if category doesn't exist in category_mean_price, add it
            category_mean_price[category]=float(price[1:])
        else: #if exists then +1
            category_mean_price[category]+=float(price[1:])
        #change string into number (for ratings)
        if all_books[title][2]=="One":
            x = 1
        elif all_books[title][2]=="Two":
            x = 2
        elif all_books[title][2]=="Three":
            x = 3
        elif all_books[title][2]=="Four":
            x = 4
        elif all_books[title][2]=="Five":
            x = 5
        books_rating = books_rating.astype('float64')
        if category not in books_rating:  #if category doesn't exist in books_rating, add it
            books_rating[category] = x
        else: #if exists then +1
            books_rating[category] += x

max = 0
min = 1000
#to find the most expensive and the cheapest books
for i in all_books:
    if max < i[0]:
        max = i[0]
    if min > i[0]:
        min = i[0]
#print(max, min)

#__________________each category mean price
for key, value in category_mean_price.items():
    category_mean_price[key] = float(value) / books_category[key] #to count the average price

#__________________each category mean rating
for key, value in books_rating.items():
    books_rating[key] = float(value) / float(books_category[key]) #to count the average rating

biggest_rating =  books_rating.nlargest(10) #to take the biggest 10 ratings off books_rating
#__________________________some prints
"""
print(category_mean_price)
print("---------------------------")
print(biggest_rating)
print("---------------------------")
print(books_rating)
print("---------------------------")
print(books_category)
print("---------------------------")
print(all_books)
print("---------------------------")
"""

#_________________category and quantity
books_category.plot(kind='bar', color='lightblue') #to make a diagram according to its categories and quantities
plt.title('Categories and Quantities')
plt.xlabel('Categories')
plt.show()

#______________each category mean price
category_mean_price.plot(kind='bar', color='pink') #to make a diagram according to its categories and its average prices
plt.title('Categories and its average prices')
plt.xlabel('Mean price')
plt.show()

#_______________Minimum and Maximum Prices
plt.plot([1, 1], [1,min], marker='o', color='pink') # to draw the cheapest book 
plt.plot([2, 2], [2, max], marker='o', color='purple') #to draw the most expensive book
plt.title('Minimum and Maximum Prices')
plt.show()

#_______________first 10 biggest rating pie diagram
plt.figure(figsize=(8, 8))  
plt.pie(biggest_rating, labels=biggest_rating.index, autopct='%1.1f%%') # to draw a pie diagram  according to the top biggest ratings 
plt.title('Ratings and categories')  
plt.show()

