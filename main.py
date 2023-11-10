from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from time import sleep
import os

def create_chrome_driver():
  global CHROME_DRIVER

  chrome_options = Options()
  chrome_options.add_experimental_option("detach", True)
  chrome_options.add_argument("--incognito")
  CHROME_DRIVER = Chrome(options=chrome_options)

def goto(url):
  CHROME_DRIVER.get(url)

def find_element(by, selector, within_element=None):
  element = None
  seconds_looking_for_element = 0

  while element == None:
    try:
      if within_element == None:
        element = CHROME_DRIVER.find_element(by, selector)
      else:
        element = within_element.find_element(by, selector)
    except NoSuchElementException:
      sleep(1)
      seconds_looking_for_element += 1
      if seconds_looking_for_element > MAX_WAIT_FOR_ELEMENT:
        print('Element not found for selector ' + selector + ' and by ' + by)
        break
      else:
        pass

  return element

def login():
  username = os.getenv('IG_USERNAME')
  password = os.getenv('IG_PASSWORD')
  username_input_label = 'Phone number, username, or email'
  username_input_selector = 'input[aria-label="' + username_input_label + '"]'
  password_input_label = 'Password'
  password_input_selector = 'input[aria-label="' + password_input_label + '"]'

  login_form = find_element(By.ID, 'loginForm')
  username_input = find_element(By.CSS_SELECTOR, username_input_selector, within_element=login_form)
  username_input.send_keys(username)
  password_input = find_element(By.CSS_SELECTOR, password_input_selector, within_element=login_form)
  password_input.send_keys(password)
  submit_button = find_element(By.CSS_SELECTOR, 'button[type="submit"]', within_element=login_form)
  submit_button.click()

def click_not_now(question):
  if question == 'turn_on_notifications':
    element_type = 'div'
  elif question == 'save_login_info':
    element_type = 'button'

  not_now_element = find_element(By.XPATH, '//' + element_type + '[text()="Not Now"]')

  if not_now_element != None:
    not_now_element.click()

def click_first_post():
  first_post = find_element(
    By.XPATH,
    '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/' + \
    'div[3]/article/div[1]/div/div[1]/div[1]/a'
  )

  if first_post != None:
    first_post.click()

def find_like_button():
  print('Looking for like button')
  # Heart svg has viewBox 0 0 48 48 when it's already liked
  # it has 0 0 24 24 when it's not liked
  svg = find_element(By.XPATH, '//svg[@aria-label="Like" and @viewBox="0 0 24 24"]')
  span = find_element(By.XPATH, './..', within_element=svg)
  div = find_element(By.XPATH, './..', within_element=span)
  return find_element(By.XPATH, './..', within_element=div)

def like_everything():
  like_counter = 0

  while like_counter < MAX_LIKES:
    if find_like_button() != None:
      like_button.click()
      like_counter += 1

    sleep(1)
    ActionChains(CHROME_DRIVER).send_keys(Keys.ARROW_RIGHT).perform()
    sleep(3)

def main():
  global MAX_WAIT_FOR_ELEMENT, MAX_LIKES
  MAX_WAIT_FOR_ELEMENT = 4
  MAX_LIKES = 2

  load_dotenv()
  create_chrome_driver()
  goto('https://instagram.com/')
  login()
  click_not_now('turn_on_notifications')
  click_not_now('save_login_info')
  goto('https://www.instagram.com/' + os.getenv('TARGET_PROFILE') + '/')
  click_first_post()
  like_everything()

if __name__ == '__main__':
  main()
