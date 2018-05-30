#!/usr/bin/python3.6
import time, requests
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup

with Display():
    # we can now start Firefox and it will run inside the virtual display
    browser = webdriver.Firefox()

    login_url = 'https://portal.mcpsmd.org/public/home.html'
    login_url_action = 'https://portal.mcpsmd.org/guardian/home.html'

# put the rest of our selenium code in a try/finally
    # to make sure we always clean up at the end
    try:
        browser.get(login_url)
        username = browser.find_element_by_id('fieldAccount')
        username.send_keys('jason.blum@gmail.com')
        password = browser.find_element_by_id('fieldPassword')
        password.send_keys('***********')
        signin = browser.find_element_by_id('btn-enter')
        signin.click()
        time.sleep(10)
        html = browser.page_source

        print(html)

        soup = BeautifulSoup(html)
        eso_grades = soup.select('#quickLookup')
        tas = browser.find_elements_by_xpath("//*[contains(text(), 'Tas')]")[0]
        tas.click()
        time.sleep(10)
        tas_grades = soup.select('#quickLookup')

        print(eso_grades)
        print(tas_grades)

        response = requests.post(
            "https://api.mailgun.net/v3/sandboxec1e86e70**************33.mailgun.org/messages",
            auth=("api", "key-eedd6a*********************5f"),
            data={"from": "Sensei Jason <jason.blum@gmail.com>",
            "to": ["jason.blum@gmail.com"],
            "subject": "Eső's and Tas' grades...",
            "html": eso_grades + tas_grades })

        print(response)
    finally:
        browser.quit()
