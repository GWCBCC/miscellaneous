'''
We bookmark so many cool things in https://groups.diigo.com/group/Pythoneers, but
I forget them over time.  I wanted a way to be reminded of them occasionally, so
I can remember to use them, check that they're still live, that they're tagged
helpfully.

So I wrote this script to use http://html.python-requests.org/ to scrape the Diigo
website and email me a random old bookmark a few times a day.
'''

import random, urllib
import urllib
from requests_html import HTMLSession
session = HTMLSession()

#What is the name of your group?
group_name = 'Pythoneers'
#*Roughly* how many times a day do you want to receive an email
number_emails_per_day = 5

#https://www.mailgun.com/
mailgun_url = 'https://api.mailgun.net/v3/sandbox###############.mailgun.org/messages'
mailgun_api_key = 'key-###########################'
from= '######################'
to = '################'

#Schedule to run hourly, but only run roughly number_emails_per_day times per day
if random.randint(1,24) <= number_emails_per_day:

    request = session.get('https://groups.diigo.com/group/' + group_name)

    last_link_elements = request.html.find('a', containing='Last »')

    last_link_element = last_link_elements[-1]

    href = last_link_element.attrs['href']

    query_string = urllib.parse.urlparse(href).query

    page_num = urllib.parse.parse_qs(query_string)['page_num'][0]

    random_page = random.randint(1, int(page_num))

    print('Browsing to page ', random_page)

    request = session.get('https://groups.diigo.com/group/' + group_name + '?view=recent&page_num=' + str(random_page))

    bookmarks = request.html.find('div .item, .middle')

    random_bookmark = random.choice(bookmarks)

    inputs = random_bookmark.find('input')

    for input in inputs:
        if 'name' in input.attrs and input.attrs['name'] == 'item_id':
            item_id = input.attrs['value']

    print('Chose bookmark id ', item_id)

    html = '<h3><a href="https://groups.diigo.com/group/Pythoneers/content/{}">EDIT THIS BOOKMARK</a>:</h3><hr/>{}'.format(item_id, random_bookmark.html)

    session.post(
        mailgun_url,
        auth=("api", mailgun_api_key),
        data={"from": from,
        "to": [to],
        "subject": "Check this Diigo bookmark",
        "html": html })

    print('Done!')
