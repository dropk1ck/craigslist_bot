# craigslist bot

Is the native craigslist search alert slow and unreliable for you? Me too! Why? I don't know! Let's automate our own.

currently:
* queries the 'for sale' page for an area and parses the resulting html with BeautifulSoup
* saves already-seen entries to a kv store (leveldb)
* can send push notifications when new items popup in search (I use pushover messages)

I assume I've already checked a search for the interesting items, so this script just focuses on new items from the first page of local listings. Someday I'll go through all the pages, but little benefit to the added complexity at this time.
