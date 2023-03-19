import requests 
from parsel import Selector
from urllib.parse import urljoin




class HackerNews():
    url = 'https://news.ycombinator.com/'


    def request(self, url):
        try:
            response = requests.get(url)
        except:
            response = None
        finally:
            return response


    def parse(self, response):
        if response:
            sel = Selector(text=response.text)
            comment_href = sel.xpath("//table//tr[2]//a[contains(text(), 'comment')]/@href").get()
            if comment_href:
                url = urljoin(self.url, comment_href)
                response = self.request(url)
                self.parse_comment(response)
    

    def parse_comment(self,response):
        if response:
            sel = Selector(text=response.text)
            top_comment = sel.xpath("(//div[@class='comment'])[1]//text()").getall()
            if top_comment:
                top_comment = "".join(list(filter(None, list(map(lambda x: x.strip() if x != 'reply' else '', top_comment)))))
                self.dump(top_comment)


    def dump(self, comment):
        with open('output.txt', 'w') as f:
            f.write(comment)


    def start_requests(self, url):
        response = self.request(url)
        self.parse(response)


    def crawl(self):
        self.start_requests(self.url)


s = HackerNews()
s.crawl()