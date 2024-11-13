from CrawlerBase import *


class CrawlerCNN(CrawlerBase):
    def __init__(self, target_url):
        super().__init__(target_url)
        pass

    def run(self):
        print('crawling :',self.target_url)
        response = requests.get(self.target_url,headers=self.headers_formed)
        self.extract_response_content(response)
        pass

    pass


def task1():
    url = 'https://edition.cnn.com/world/europe'
    ins = CrawlerCNN(url)
    ins.set_referred_url("https://edition.cnn.com")
    ins.run()
    pass


if __name__ == '__main__':
    task1()
    pass
