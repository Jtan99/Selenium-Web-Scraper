from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import numpy as np

def getItemsInPage(page):
  items_node = page.find_elements(by=By.ID, value="gridItemRoot")
  items = []
  for item_node in items_node:
    title = "unavailable"
    average = "unavailable"
    reviews = "unavailable"
    price = "unavailable"
    
    try:
      title = item_node.find_element(by=By.XPATH, value=".//div//div[last()]//a[2]").text
      average = item_node.find_element(by=By.CLASS_NAME, value="a-icon-alt").get_attribute('innerHTML')
      reviews = item_node.find_element(by=By.XPATH, value=".//div/div[last()]/div/div[1]").text
      price = item_node.find_element(by=By.XPATH, value=".//div/div[last()]/div/div[2]").text
    except NoSuchElementException:
        pass
    item = [title,average,reviews,price]
    items.append(item)
  print(items)
  return items

if __name__ == "__main__":
  # Setting selenium options
  options = Options()
  options.headless = True
  options.add_argument("--disable-extensions")
  options.add_argument("--window-size=1920,1200")
  browser = webdriver.Chrome(options=options)

  # Code starts below
  BASE_URL = ""   ## intentionally removed
  browser.get(BASE_URL)
  base_window = browser.current_window_handle

  DEPARTMENTS_LINK_NODE = browser.find_elements(by=By.XPATH, value="//div[@role='treeitem']//a")
  count = 1
  data = []
  for department_link_node in DEPARTMENTS_LINK_NODE:
    department_url = department_link_node.get_attribute('href')

    department_link_node.send_keys(Keys.CONTROL + Keys.ENTER)
    browser.switch_to.window(browser.window_handles[1])
    data += getItemsInPage(browser)
    
    sleep(np.random.uniform(2, 5))   ##adding a sleep here to slow down requests
    browser.close()
    browser.switch_to.window(base_window)
    count += 1
  np.array(data)
  np.savetxt('myfile.csv', data, fmt='%s', delimiter=',')

  browser.save_screenshot("test.png")
  browser.quit()