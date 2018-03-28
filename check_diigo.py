'''
We bookmark so many cool things in https://groups.diigo.com/group/Pythoneers, but
I forget them over time.  I wanted a way to be reminded of them occasionally, so
I can remember to use them, check that they're still live, that they're tagged
helpfully.

So I wrote this script to use http://html.python-requests.org/ to scrape the Diigo
website and email me a random old bookmark a few times a day.

I'd recommend running this in a virtual environment:
1) download Python 3.6+
2) create a folder and stick a virtualenv in it (https://docs.python.org/3/library/venv.html)
3) Schedule a cron job to run the script in that environment every hour:
0 * * * * /Users/jasonblum/diigo/bin/python /Users/jasonblum/diigo/check_diigo.py

BTW, yes, I know they have an API (https://www.diigo.com/api_dev) but, after multiple
exchanges with their technical support, I could never seem to get it to work.  And anyway
python-requests makes it almost just as easy!
'''

import random, urllib
import urllib
from requests_html import HTMLSession
session = HTMLSession()

#What is the name of your group?
group_name = 'Pythoneers'
#*Roughly* how many times a day do you want to receive an email, assuming this job is running around the clock?
number_emails_per_day = 5

#https://www.mailgun.com/
mailgun_url = 'https://api.mailgun.net/v3/sandbox###############.mailgun.org/messages'
mailgun_api_key = 'key-###########################'
from= '######################'
to = '################'

#Schedule to run hourly, but only run roughly number_emails_per_day times per day
if random.randint(1,24) <= number_emails_per_day:

    #Go get the main page.
    request = session.get('https://groups.diigo.com/group/' + group_name)

    #Now pick a random page from this group's history:
    last_link_elements = request.html.find('a', containing='Last »')
    last_link_element = last_link_elements[-1]
    href = last_link_element.attrs['href']
    query_string = urllib.parse.urlparse(href).query
    page_num = urllib.parse.parse_qs(query_string)['page_num'][0]
    random_page = random.randint(1, int(page_num))
    print('Browsing to page ', random_page)

    #Now get a random bookmark on that page:
    request = session.get('https://groups.diigo.com/group/' + group_name + '?view=recent&page_num=' + str(random_page))
    bookmarks = request.html.find('div .item, .middle')
    random_bookmark = random.choice(bookmarks)
    inputs = random_bookmark.find('input')
    for input in inputs:
        if 'name' in input.attrs and input.attrs['name'] == 'item_id':
            item_id = input.attrs['value']
    print('Chose bookmark id ', item_id)

    #Now, send the email!
    html = '<h1><a href="https://groups.diigo.com/group/Pythoneers/content/{}">EDIT THIS BOOKMARK</a>:</h1>&nbsp;<p/>&nbsp;<hr/>{}'.format(item_id, random_bookmark.html)
    session.post(
        mailgun_url,
        auth=("api", mailgun_api_key),
        data={"from": from,
        "to": [to],
        "subject": "Check this Diigo bookmark",
        "html": html })

    print('Done!')
