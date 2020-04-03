# craigslist bot

Can't find a reliable online tool to get notified of new craigslist items? Me either. CL has native search alerts, and they work some time. I wanted something faster and more reliable that would give me push alerts.

currently:
* queries the 'for sale' page for an area and parses the resulting html with BeautifulSoup
* saves already-seen entries to a kv store (leveldb)
* can send push notifications when new items popup in search (I use pushover messages)

I assume I've already checked a search for the interesting items, so this script just focuses on new items from the first page of local listings.
