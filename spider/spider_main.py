from spider import url_manage, html_downloader, html_parser, html_outputer
from bs4 import BeautifulSoup
from urllib import request
import re


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manage.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.titles = []
        self.pictures = []
        self.links = []

    def dep_craw(self, url):
        r = request.urlopen(url)
        html = r.read()
        soup = BeautifulSoup(html, 'html.parser', from_encoding='GB2312')
        picture = soup.find('img', src=re.compile(r"https:(.*?).jpg"))
        picture_link = picture['src']
        movie_name = soup.find('font', color="#07519a").get_text()
        link = soup.find('a', href=re.compile(r"ftp://(.*?).mkv"))
        link = link['href']
        return movie_name, picture_link, link

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                # print('craw %d : %s' % (count, new_url))
                html_count = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_count)
                for url in new_urls:
                    movie_name, picture_link, link = self.dep_craw(url)
                    self.titles.append(movie_name)
                    self.pictures.append(picture_link)
                    self.links.append(link)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count == 1000:
                    break
                count = count + 1
            except:
                print('crawl failed')
            self.outputer.output_html()
        return self.titles, self.pictures, self.links


if __name__ == "__main__":
    for i in range(1, 43):
        # https://www.dytt8.net/html/gndy/china/list_4_2.html
        root_url = "https://www.dytt8.net/html/gndy/china/list_4_"+str(i)+".html"
        obj_spider = SpiderMain()
        titles, pictures, links = obj_spider.craw(root_url)
        print(titles, pictures, links)

