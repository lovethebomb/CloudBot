"""Searches wikipedia and returns first sentence of article
Scaevolus 2009"""
# -*- coding: utf-8 -*-

import re

from util import hook, http, text

api_prefix_en = "http://en.wikipedia.org/w/api.php"
api_prefix_fr = "http://fr.wikipedia.org/w/api.php"
params = "?action=opensearch&format=xml"

paren_re = re.compile('\s*\(.*\)$')

@hook.command('w')
@hook.command
def wiki_en(inp):
    search_url = api_prefix_en + params
    get_items(inp, search_url)

@hook.command('w_fr')
@hook.command
def wiki_fr(inp):
    search_url = api_prefix_fr + params
    get_items(inp, search_url)

def get_items(inp, url_query):
    """wiki <phrase> -- Gets first sentence of Wikipedia article on <phrase>."""
    #print url_query
    x = http.get_xml(url_query, search=inp)
    #print x
    ns = '{http://opensearch.org/searchsuggest2}'
    items = x.findall(ns + 'Section/' + ns + 'Item')
    
    if not items:
        if x.find('error') is not None:
            #print 'error: %(code)s: %(info)s' % x.find('error').attrib
            return 'error: %(code)s: %(info)s' % x.find('error').attrib
        else:
            #print 'Le results not found'
            return 'Le results not found'

    def extract(item):
        return [item.find(ns + x).text for x in
                            ('Text', 'Description', 'Url')]
    
    title, desc, url = extract(items[0])

    if 'may refer to' in desc:
        title, desc, url = extract(items[1])

    title = paren_re.sub('', title)

    if title.lower() not in desc.lower():
        desc = title + desc

    desc = re.sub('\s+', ' ', desc).strip()  # remove excess spaces
    desc = text.truncate_str(desc, 200).encode("utf-8")

    #print '{} :: {}'.format(desc, http.quote(url, ':/'))
    return '{} :: {}'.format(desc, http.quote(url, ':/'))

