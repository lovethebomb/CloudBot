"""Searches wikipedia and returns first sentence of article
Scaevolus 2009"""

import re

from util import hook, http, text


api_prefix = "http://en.wikipedia.org/w/api.php"
search_url = api_prefix + "?action=opensearch&format=xml"
search_url_fr = api_prefix + search_url + "&prop=langlinks&lllang=fr"

paren_re = re.compile('\s*\(.*\)$')


@hook.command('w')
@hook.command
def wiki_en(inp):
    get_items(inp, search_url)

@hook.command('wfr')
@hook.command
def wiki_fr(inp):
    get_items(inp, search_url_fr)

def get_items(inp, url_query):
    """wiki <phrase> -- Gets first sentence of Wikipedia article on <phrase>."""
    x = http.get_xml(url_query, search=inp)
    ns = '{http://opensearch.org/searchsuggest2}'
    items = x.findall(ns + 'Section/' + ns + 'Item')
    
    if not items:
        if x.find('error') is not None:
            return 'error: %(code)s: %(info)s' % x.find('error').attrib
        else:
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
    desc = text.truncate_str(desc, 200)

    return '{} :: {}'.format(desc, http.quote(url, ':/'))

