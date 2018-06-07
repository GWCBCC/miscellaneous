#!/usr/bin/python3.6
# Note on pythonanywhere, we have to use selenium<3 per https://help.pythonanywhere.com/pages/selenium/
# pip install requests pyvirtualdisplay "selenium<3"
import time, requests
from pyvirtualdisplay import Display
from selenium import webdriver

with Display():
    # Theyre doing tons of weird javascript and I could only get the page to work by specifying a user agent
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11;     Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0   Safari/537.36")

    browser = webdriver.Firefox(profile)

    login_url = 'https://portal.mcpsmd.org/public/home.html'
    login_url_action = 'https://portal.mcpsmd.org/guardian/home.html'

    # put the rest of our selenium code in a try/finally
    # to make sure we always clean up at the end
    try:
        browser.get(login_url)
        username = browser.find_element_by_id('fieldAccount')
        username.send_keys('jason.blum@gmail.com')
        password = browser.find_element_by_id('fieldPassword')
        password.send_keys('5Q*******#b')
        signin = browser.find_element_by_id('btn-enter')
        signin.click()
        time.sleep(10)

        eso_grades = browser.find_element_by_id('content-main').get_attribute('innerHTML')

        tas = browser.find_elements_by_xpath("//*[contains(text(), 'Tas')]")[0]
        tas.click()
        time.sleep(10)

        tas_grades = browser.find_element_by_id('content-main').get_attribute('innerHTML')

        response = requests.post(
            "https://api.mailgun.net/v3/sandboxec1e86e7*********2733.mailgun.org/messages",
            auth=("api", "key-eedd6ade**********85f"),
            data={"from": "Sensei Jason <jason.blum@gmail.com>",
            "to": ["jason.blum@gmail.com"],
            "subject": "Eső's and Tas' grades...",
            "html": eso_grades + tas_grades })

        print('Response from mailgun: ', response)
        print('Response from mailgun: ', response.text)
    finally:
        browser.quit()
