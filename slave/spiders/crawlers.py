#-*-coding:utf-8-*-
import urllib2

import re

from bs4 import BeautifulSoup


class SimpleCrawler:
    def __init__(self, start_url, allowed_domain):
        """

        :param start_url:
        :param domain:
        """
        self.start_url = start_url
        self.allowed_domain = allowed_domain
        self.header = {
            "User-Agent": "Mozilla-Firefox5.0"
        }

    def fetch(self, url):
        """fetch content of webpage"""
        self.url = url_encode(url)
        request = urllib2.Request(self.url)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            response = urllib2.urlopen(request)
            self.content = response.read()
            self.success = True
        except Exception, e:
            print e
            self.success = False

    def parse(self):
        """parse the content of html and extract next url"""
        if not self.url:
            print "Cannot parse before fetch!"
            raise RuntimeError

        soup = BeautifulSoup(self.content, "lxml")
        item = {
            "title": self.extract_title(soup),
            "content": self.extract_content(soup),
            "href": self.url,
            "links": self.extract_links(soup),
            "raw_content": self.content
        }
        return item

    def extract_title(self, soup):
        """
            extract title of html
            :param soup:
        """
        return soup.title.string

    def extract_content(self, soup):
        """
            extract main content of html
            :param soup:
        """

        # remove script tag and style tag
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        soup.prettify()

        reg = re.compile("<[^>]*>")
        content = reg.sub('', soup.prettify()).strip()
        content = " ".join(content.split())
        return content

    def extract_links(self, soup):
        """
            extract all valid link from html
            :param soup:
        """
        next_urls = []
        soup_url_list = soup.find_all("a")

        for soup_url in soup_url_list:
            url = soup_url.get("href")

            # if there is any url in html
            if url and not ("mailto" in url):
                if self.allowed_domain in url:
                    next_urls.append(url)

                elif len(url) and url[0] == '/':
                    # Handle relative path
                    url = self.start_url + url
                    next_urls.append(url)

        return next_urls


def url_encode(str):
    repr_str = repr(str).replace(r'\x', '%')
    return repr_str[1:-1]


# test = SimpleCrawler("http://jetmuffin.github.io", "jetmuffin.github.io")
# test.fetch("http://jetmuffin.github.io")
# item = test.parse()
# for link in item['links']:
#     print link

# print url_encode("http://jetmuffin.github.io/tags/计信院程序设计大赛/")