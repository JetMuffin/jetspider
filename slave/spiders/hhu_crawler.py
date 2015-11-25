import urllib2
from bs4 import BeautifulSoup

class HHUCrawler:

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
        self.url = url
        request = urllib2.Request(url)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            response = urllib2.urlopen(request)
            self.content = response.read()
            self.success = True
        except Exception, e:
            self.success = False

    def parse(self):
        """parse the content of html and extract next url"""
        if not self.url:
            print "Cannot parse before fetch!"
            raise RuntimeError

        next_urls = []
        soup = BeautifulSoup(self.content, "lxml")
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

        return  next_urls

