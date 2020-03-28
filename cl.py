#!/usr/bin/env python3

import argparse
import plyvel
import requests
import urllib
from bs4 import BeautifulSoup
from pushover import send_message

def log(msg):
    print(msg)


def do_search(location, searchterm, db, ignorefirst):
    #URL = urllib.parse.urlencode('https://{}.craigslist.org/search/sss?query={}'.format(location, searchterm))
    URL = 'https://{}.craigslist.org/search/sss?query={}'.format(location, searchterm)

    doc = requests.get(URL)
    if doc.status_code != 200:
        log('bad HTTP return code for searchterm {}'.format(searchterm))
        return False

    soup = BeautifulSoup(doc.text, 'html.parser')

    # lets see how many total results there are; craigslist seems to use the class 'totalcount'
    # for the page element that displays the total search results
    total_count = soup.find_all(name='span', attrs={'class': 'totalcount'})
    if len(total_count) < 1:
        log('did not find total results count on page')
        return False

    total_count = int(total_count[0].contents[0])
    log('[+] total search results: {}'.format(total_count))

    # how many results on this page? rangeTo is the upper bound on the highest-numbered
    # result shown on this page
    range_to = soup.find_all(name='span', attrs={'class': 'rangeTo'})
    if len(range_to) < 1:
        log('did not find range_to on page')
        return False
    
    log('============ {} ============'.format(searchterm))
    range_to = int(range_to[0].contents[0])
    log('[+] results on this page: {}'.format(range_to))

    # iterate the search results, bounding ourselves at the number of results in the current page
    for i, result in enumerate(soup.find_all(name='p', attrs={'class': 'result-info'})):
        if i >= range_to:
            # once we're above rangeTo, we're no longer in 'local' search results
            # just bail at this point
            break
    
        result_link_tag = result.find(name='a', attrs={'class': 'result-title hdrlnk'})
        result_id = result_link_tag['data-id']
        result_name = result_link_tag.contents[0]
        result_link = result_link_tag['href']

        # custom func I use to notify my smartphone of a new listing
        #send_message('New search result: ' + result_name + '\n' + result_link)

        # add this to the db if it doesn't exist
        if db.get(bytes(result_id, 'utf-8')) is None:
            db.put(bytes(result_id, 'utf-8'), bytes(result_name, 'utf-8'))
            print('New item: {}'.format(result_name))

    log('[+] done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', default='newyork', help='specify which craigslist to search')
    parser.add_argument('--ignorefirst', default='False', help='do *not* send notifications for new listings during first search')
    parser.add_argument('searchterms', help='a comma-separated list of search terms (e.g. "toilet paper,hand sanatizer,macbook pro"')
    args = parser.parse_args()

    # connect to leveldb, or create the db if necessary
    db = plyvel.DB('./db', create_if_missing=True)

    searchterms = args.searchterms.split(',')
    for searchterm in searchterms:
        do_search(args.location, searchterm, db, args.ignorefirst)

    db.close()

