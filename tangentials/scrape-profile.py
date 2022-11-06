import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
# import EC
from selenium.webdriver.support import expected_conditions as EC

# open https://www.goodreads.com/review/list/138558406?shelf=read#

books = []

driver = webdriver.Firefox()
driver.get("https://www.goodreads.com/review/list/138558406?shelf=read#")
# wait for load
sleep(4)
# reload the page
driver.refresh()
sleep(2)

links = {}
# find all links which have "book/show" in href
book_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'book/show')]")

last_number_of_books = 0
number_of_books = 1
# while the number of books is changing, scroll to the bottom of the page and wait
while last_number_of_books != number_of_books:
    last_number_of_books = number_of_books
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)
    book_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'book/show')]")
    number_of_books = len(book_links)
    
for link in book_links:
    url = link.get_attribute("href").split('/')[-1].split('.')[0].split('-')[0]
    # print parent of parent of parent using By.XPATH
    parent = link.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").text
    # set rating from 1 to 5 depending which string can be found in parent
    rating = None
    if 'it was amazing' in parent:
        rating = 5
    elif 'really liked it' in parent:
        rating = 4
    elif 'liked it' in parent:
        rating = 3
    elif 'it was ok' in parent:
        rating = 2
    elif 'did not like it' in parent:
        rating = 1
    
    # add to dictionary
    links[url] = rating

# <span class=" staticStars notranslate" title="did not like it"><span size="15x15" class="staticStar p10">did not like it</span><span size="15x15" class="staticStar p0"></span><span size="15x15" class="staticStar p0"></span><span size="15x15" class="staticStar p0"></span><span size="15x15" class="staticStar p0"></span></span>
# remove duplicates
print(links)

