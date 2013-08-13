from util import hook, http, urlnorm
from bs4 import BeautifulSoup

base_url = "http://www.estcequecestbientotleweekend.fr"


@hook.command(autohelp=False)
def weekend(inp):
    "weekend -- est-ce que c'est bientot le weekend ?"
    url = urlnorm.normalize(base_url.encode('utf-8'), assume_scheme="http")

    try:
        page = http.open(url)
        soup = BeautifulSoup(page.read())
    except (http.HTTPError, http.URLError):
        return "Could not fetch page."

    msg = soup.find(class_="msg").string

    if not msg:
        return "Could not find title."

    return u"Bientot le week-end? {}".format(msg)
