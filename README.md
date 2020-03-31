# craigslist bot

currently:
* queries the 'for sale' page for an area and parses the resulting html with BeautifulSoup
* saves already-seen entries to a kv store (leveldb)
* can send push notifications when new items popup in search 


will shortly:
* handle multi-page results
* real logging of some kind
