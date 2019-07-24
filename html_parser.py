from urllib import parse
from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/html/tv/rihantv/\d+/\d+.html"))
        for link in links:
            new_url = link['href']
            new_full_url = parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url
        title_node = soup.find('a', class_="ulink")
        if title_node is None:
            return
        res_data['title'] = title_node.get_text()
        return res_data

    def parse(self, page_url, html_count):
        if page_url is None or html_count is None:
            return
        soup = BeautifulSoup(html_count, 'html.parser', from_encoding='GB2312')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data





        

