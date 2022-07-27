from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import numpy as np
import csv
import re

BASE_URL = ""
FILE_NAME = "./data/reviews2.csv"
MAX_PAGES = 2   ##more pages = more data

##  Function to highlight an element, used for debugging purposes 
def highlight(element):
  d = element._parent
  def apply_style(s):
    d.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)
  original_style = element.get_attribute('style')
  apply_style("background: yellow; border: 2px solid red;")
  sleep(1)
  apply_style(original_style)

def get_review_details(root):
  rating = root.find_element(by=By.XPATH, value=".//span[contains(@class, 'a-icon-alt')]").get_attribute('innerHTML')
  title = root.find_element(by=By.XPATH, value=".//*[contains(@class, 'review-title')]/span").get_attribute('innerHTML')
  date_location = root.find_element(by=By.XPATH, value=".//span[contains(@class, 'review-date')]").get_attribute('innerHTML')

  description = ""
  try:
    description = root.find_element(by=By.XPATH, value=".//span[contains(@class, 'review-text')]/span").get_attribute('innerHTML')
  except NoSuchElementException:
    pass

  verified = "non-verified"
  try:
    verified = root.find_element(by=By.XPATH, value="").get_attribute('innerHTML')
  except NoSuchElementException:
    pass
  
  helpful = "0"
  try:
    helpful = root.find_element(by=By.XPATH, value="").get_attribute('innerHTML')
  except NoSuchElementException:
    pass
  # print([rating, title, date_location, description, verified, helpful])
  return [rating, title, date_location, description, verified, helpful]


def is_reviews_page(url):
  pass

if __name__ == "__main__":
  options = Options()
  options.headless = True
  options.add_argument("--disable-extensions")
  options.add_argument("--window-size=1920,1200")
  browser = webdriver.Chrome(options=options)

  browser.get(BASE_URL)

  if(not(is_reviews_page(BASE_URL))):
    new_url = BASE_URL
    new_url = re.sub(r"", "", new_url)
    browser.get(new_url)

  page = 1
  reviews = []
  f = open(FILE_NAME, 'w', newline='', encoding='utf-8')
  while True:
    sleep(np.random.uniform(2, 5)) ##adding a sleep here to slow down requests
    if(page>MAX_PAGES):
      break
    print("page", page)
    try:
      reviews_node = browser.find_elements(by=By.XPATH, value="//div[starts-with(@id, 'customer_review')]")
      for review_node in reviews_node:
        reviews = [get_review_details(review_node)]
        csv.writer(f).writerows(reviews)
      
      sleep(np.random.uniform(5, 10))   ##adding a sleep here to slow down requests
      next_node = browser.find_element(by=By.CSS_SELECTOR, value=".a-last a")
      next_node.click()
    except (NoSuchElementException):
      break
    page += 1

  browser.save_screenshot("test.png")
  f.close()
  browser.quit()