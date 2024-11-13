from CrawlerBase import *


# 基本的请求头
# 目标URL

class CrawlCBS(BatchCrawler):
    def __init__(self, target_url, result_txt_file_name, crawl_number):
        super().__init__(target_url, result_txt_file_name, crawl_number)
        pass

    pass


def task1():
    url = 'https://www.cbsnews.com/world/'
    crawl_number = 3
    ins = CrawlCBS(url, '', crawl_number)
    ins.run()
    pprint(ins.link_text_link_url_tuple_list)
    pass


def task2():
    url = "https://www.cbsnews.com/news/qantas-emergency-landing-engine-failure-australia/"
    ins = BatchCrawler(url, '', 1)
    ins.extract_response_content(ins.response, 'cbsnewstest.txt')
    pass


if __name__ == '__main__':
    task1()
    pass
