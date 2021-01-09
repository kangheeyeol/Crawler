import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def crawling_review(html):
    soup = BeautifulSoup(html, 'html.parser')
    lists = soup.findAll('q', {'class': 'IRsGHoPm'})

    for item in lists:
        review = item.get_text()
        print(review)


def crawling_hotel(html):
    soup = BeautifulSoup(html, 'html.parser')
    lists = soup.findAll('div', {'class': 'listing_title'})

    for item in lists:
        title = item.get_text()
        print(title)


def search():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('lang=ko_KR')
    chromedriver_path = "/Users/jerald/Downloads/chromedriver"
    review_url = \
        "https://www.tripadvisor.co.kr/Hotel_Review-g294197-d12310284-Reviews-Signiel_Seoul-Seoul.html"
    # "https://www.tripadvisor.co.kr/Hotel_Review-g294197-d20886229-Reviews-Mondrian_Seoul_Itaewon-Seoul.html#REVIEWS"
    driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)

    driver.get(review_url)
    driver.implicitly_wait(3)

    for i in range(10):
        html = driver.page_source
        crawling_review(html)
        try:
            driver.find_element_by_link_text('다음').click()
            sleep(1)
            print("Next Page")
        except NoSuchElementException:
            print("Review page End")

    driver.quit()


def hotel_list():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('lang=ko_KR')
    chromedriver_path = "/Users/jerald/Downloads/chromedriver"
    hotel_url = \
        "https://www.tripadvisor.co.kr/Hotels-g294197-Seoul-Hotels.html#BODYCON"
    driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)

    driver.get(hotel_url)
    driver.implicitly_wait(3)

    for i in range(10):
        html = driver.page_source
        # print(html)k
        crawling_hotel(html)
        try:
            driver.find_element_by_link_text('다음').click()
            sleep(5)
            print("Next Page")
        except NoSuchElementException:
            print("Review page End")

    driver.quit()


def main():
    hotel_list()
    # search()
    print("finish")


if __name__ == '__main__':
    main()
