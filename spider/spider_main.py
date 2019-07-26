from spider import url_manage, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manage.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                # print('craw %d : %s' % (count, new_url))
                html_count = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_count)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if count == 1000:
                    break
                count = count + 1
            except:
                print('crawl failed')
            print(new_data)
            self.outputer.output_html()


if __name__ == "__main__":
    for i in range(1, 43):
        # https://www.dytt8.net/html/tv/rihantv/list_8_2.html
        root_url = "https://www.dytt8.net/html/tv/rihantv/list_8_"+str(i)+".html"
        obj_spider = SpiderMain()
        obj_spider.craw(root_url)