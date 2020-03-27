#!/usr/bin/env python3

import plyvel
import requests
from bs4 import BeautifulSoup
from pushover import send_message

def log(msg):
    print(msg)


def do_search(location, query_param):
    URL = 'https://{}.craigslist.org/search/sss?query={}'.format(location, query_param)

    doc = requests.get(URL)
    if doc.status_code != 200:
        log('bad HTTP return code')
        return False

    soup = BeautifulSoup(doc.text, 'html.parser')

    # lets see how many total results there are
    total_count = soup.find_all(name='span', attrs={'class': 'totalcount'})
    if len(total_count) < 1:
        log('did not find total results count on page')
        return False

    total_count = int(total_count[0].contents[0])
    log('[+] total search results: {}'.format(total_count))

    # how many results on this page?
    range_to = soup.find_all(name='span', attrs={'class': 'rangeTo'})
    if len(range_to) < 1:
        log('did not find range_to on page')
        return False

    range_to = int(range_to[0].contents[0])
    log('[+] results on this page: {}'.format(range_to))

    # iterate of the search results
    for i, result in enumerate(soup.find_all(name='p', attrs={'class': 'result-info'})):
        #if i >= range_to:
        if i > 0:
            # we're likely no longer in 'local' search results, bail
            break
    
        log('================\n\n' + str(result) + '\n\n\n')
        result_link_tag = result.find(name='a', attrs={'class': 'result-title hdrlnk'})
        result_id = result_link_tag['data-id']
        result_name = result_link_tag.contents[0]
        result_link = result_link_tag['href']

        log('data-id: {}'.format(result_id))
        log('name: {}'.format(result_name))
        log('link: {}'.format(result_link))
        # custom func I use to notify my smartphone of a new listing
        send_message('New search result: ' + result_name + '\n' + result_link)

    log('[+] done')


if __name__ == '__main__':
    do_search('newyork', 'macbook')

