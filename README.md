Homerun
=======

Crawls real estate sites for houses in Bergisch Gladbach.

Dependencies
------------

- Python 2.7
- BeautifulSoup 3

Fetching houses
---------------

The following command will crawl real estate sites and store all the
houses it finds in _houses.json_:

    bin/fetch_houses

New houses have the `new` property set to `true`.

Printing houses
---------------

This prints all the houses from _houses.json_, sorted by price:

    bin/print_houses
