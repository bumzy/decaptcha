#!/usr/bin/env python3
import sys
from PIL import Image
from io import BytesIO
import re
import logging
if sys.version > '3':
    from urllib.parse import urljoin
    from html.parser import HTMLParser
    from urllib.request import Request, urlopen
else:
    from urlparse import urljoin
    from HTMLParser import HTMLParser
    from urllib2 import Request, urlopen


class _CaptchaParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.captcha_src = ''

    def handle_startendtag(self, tag, attributes):
        if tag != 'img':
            return

        flag = 0
        img_src = ''

        for name, value in attributes:
            if name == 'alt' and value == 'CAPTCHA':
                flag = 1
            if name == 'src':
                img_src = value

        if flag:
            self.captcha_src = img_src


def get_captcha_link(login_url):
    if not re.match(r'^https?:/{2}\w.+$', login_url):
        logging.error('login_url is invalid')
        return
    req = Request(login_url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36')
    html = urlopen(req).read().decode("utf-8")
    parser = _CaptchaParser()
    parser.feed(html)
    captcha_src = parser.captcha_src
    parser.close()
    return urljoin(login_url, captcha_src)


def get_captcha_image(login_url):
    captcha_link = get_captcha_link(login_url)
    if captcha_link is None:
        return
    logging.debug('captcha_link: %s' % captcha_link)
    captcha_file = BytesIO(urlopen(captcha_link).read())
    captcha_image = Image.open(captcha_file)
    return captcha_image
