# -*- coding: utf-8 -*-
"""
@time   : 2021-1-27 15:45
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import requests


class ArticleNotFound(RuntimeError):
    """ Article query returned no results """


class Client(requests.Session):

    def __init__(self, lang="en"):
        super(Client, self).__init__()
        self.base_url = 'https://' + lang + '.wikipedia.org/w/api.php'

    def fetch_page(self, title, method='GET', only_body=False):
        """ Query for page by title """
        params = {'prop': 'revisions',
                  'format': 'json',
                  'action': 'query',
                  'explaintext': '',
                  'titles': title,
                  'rvprop': 'content'}
        r = self.request(method, self.base_url, params=params)
        r.raise_for_status()
        pages = r.json()["query"]["pages"]
        # use key from first result in 'pages' array
        pageid = list(pages.keys())[0]
        if pageid == '-1':
            raise ArticleNotFound('no matching articles returned')
        if not only_body:
            return pages[pageid]
        return pages[pageid]['revisions'][0]['*']
