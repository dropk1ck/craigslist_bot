import plyvel
from cl import do_search

def test_search():
    location = 'newyork'
    searchterm = 'bike'
    db = plyvel.DB(location, create_if_missing=True)
    assert do_search(location, searchterm, db, False) == True

