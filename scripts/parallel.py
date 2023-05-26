# from dotenv import load_dotenv
import os
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from threading import Thread

# load_dotenv()
BROWSER_STACK_USERNAME = os.environ["username"]
BROWSERSTACK_ACCESS_KEY = os.environ["access_key"]
URL = "https://hub.browserstack.com/wd/hub"
BROWSERSTACK_BUILD_NAME='build'

capabilities = [
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "buildName": "browserstack-build-1",
        "sessionName": "BStack parallel python",
        "browserName": "Firefox",
        "browserVersion": "latest"
    },
    {
        "os": "Windows",
        "osVersion": "10",
        "buildName": "browserstack-build-1",
        "sessionName": "BStack parallel python",
        "browserName": "Chrome",
        "browserVersion": "latest"
    },
    {
        "osVersion": "12.0",
        "deviceName": "Samsung Galaxy S22",
        "buildName": "browserstack-build-1",
        "sessionName": "BStack parallel python",
        "browserName": "chrome",
    },
]


def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "edge": EdgeOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())


def run_session(cap):
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    if "deviceName" in cap:
        bstack_options['deviceName'] = cap["deviceName"]
    bstack_options["source"] = "python:sample-main:v1.1"
    if cap['browserName'] in ['ios']:
        cap['browserName'] = 'safari'
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    if cap['browserName'].lower() == 'samsung':
        options.set_capability('browserName', 'samsung')
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)
    try:
        # navigates to browserstack
        driver.get('https://www.browserstack.com/users/sign_in')
        driver.maximize_window()
        WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, "user_email_login")))
        email_field = driver.find_element(By.ID, "user_email_login")
        password_field = driver.find_element(By.ID, "user_password")
        signin = driver.find_element(By.NAME, "commit")

        signin_action = ActionChains(driver)
        signin_action.send_keys_to_element(email_field, os.getenv('BROWSER_STACK_EMAIL'))

        signin_action.send_keys_to_element(password_field, os.getenv('BROWSER_STACK_PW'))
        signin_action.click(signin)
        signin_action.perform()

        # invite
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "invite-link")))
        invite_link = driver.find_element(By.ID, "invite-link")
        invite_action = ActionChains(driver)
        # assert the invite link is on the page
        assert invite_link
        # click the invite link
        invite_action.click(invite_link)
        invite_action.perform()

        # copy code
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "manage-users__invite-copy-cta")))
        driver.find_element(By.CLASS_NAME, "manage-users__invite-copy-cta").click()

        #logout
        WebDriverWait(driver, timeout=10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "account-dropdown-toggle")))
        account_dropdown = driver.find_element(By.CLASS_NAME, "account-dropdown-toggle")
        logout_action = ActionChains(driver)
        logout_action.move_to_element(account_dropdown)
        # sign out link
        sign_out_link = driver.find_element(By.ID, "sign_out_link")
        logout_action.move_to_element(sign_out_link)
        logout_action.click(sign_out_link)
        logout_action.perform()

        # test code

        # driver.get("https://bstackdemo.com/")
        # WebDriverWait(driver, 10).until(EC.title_contains("StackDemo"))
        # # Get text of an product - iPhone 12
        # item_on_page = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, '//*[@id="1"]/p'))).text
        # # Click the 'Add to cart' button if it is visible
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #     (By.XPATH, '//*[@id="1"]/div[4]'))).click()
        # # Check if the Cart pane is visible
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #     (By.CLASS_NAME, "float-cart__content")))
        # # Get text of product in cart
        # item_in_cart = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #     (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div[2]/div/div[3]/p[1]'))).text
        # # Verify whether the product (iPhone 12) is added to cart
        # if item_on_page == item_in_cart:
        #     # Set the status of test as 'passed' or 'failed' based on the condition; if item is added to cart
        #     driver.execute_script(
        #         'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "code as been copied"}}')
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
    # Stop the driver
    driver.quit()


for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()
