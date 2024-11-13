from CrawlerBase import *
from CrawlerBaseExclusion import *

exclusion = """https://newsukraine.rbc.ua/
ua https://www.rbc.ua/
x https://x.com/NewsUkraineRBC
en javascript:;
https://newsukraine.rbc.ua/search
https://www.facebook.com/NewsUkraineRBC/
ru https://www.rbc.ua/ukr
War in Ukraine https://newsukraine.rbc.ua/war-in-ukraine
Life https://newsukraine.rbc.ua/life
World https://newsukraine.rbc.ua/world
Politics https://newsukraine.rbc.ua/politics
Business https://newsukraine.rbc.ua/business
Opinion https://newsukraine.rbc.ua/opinion
People https://newsukraine.rbc.ua/people
US elections https://newsukraine.rbc.ua/tag/us-elections
Georgia elections https://newsukraine.rbc.ua/tag/georgia
Kursk operation https://newsukraine.rbc.ua/tag/russian-border-breach
Middle East conflict https://newsukraine.rbc.ua/tag/israel
President Zelenskyy https://newsukraine.rbc.ua/tag/volodymyr-zelenskyy
News https://newsukraine.rbc.ua/news
Articles https://newsukraine.rbc.ua/articles
Interview https://newsukraine.rbc.ua/interview
War in Ukraine https://newsukraine.rbc.ua/war-in-ukraine
Life https://newsukraine.rbc.ua/life
World https://newsukraine.rbc.ua/world
Politics https://newsukraine.rbc.ua/politics
Business https://newsukraine.rbc.ua/business
Opinion https://newsukraine.rbc.ua/opinion
People https://newsukraine.rbc.ua/people
US elections https://newsukraine.rbc.ua/tag/us-elections
Georgia elections https://newsukraine.rbc.ua/tag/georgia
Kursk operation https://newsukraine.rbc.ua/tag/russian-border-breach
Middle East conflict https://newsukraine.rbc.ua/tag/israel
President Zelenskyy https://newsukraine.rbc.ua/tag/volodymyr-zelenskyy
Follow us on X. Get the latest news https://x.com/NewsUkraineRBC
"""
OPEN = 1
CLOSED = 0


class CrawlerNewsUkraineRbcUa(CrawlerBase):
    def __init__(self, target_url, result_txt_file_name=None, crawl_number=15):
        super().__init__(target_url, result_txt_file_name)
        self.target_url = target_url
        self.crawl_number = crawl_number
        if result_txt_file_name:
            self.result_txt_file_name = result_txt_file_name
            pass
        else:
            self.result_txt_file_name = 'news_ukraine_rbc_crawl_results_{}.txt'.format(moment())
            pass
        #
        self.headers_formed = {}
        self.link_text_link_url_tuple_list = []
        #
        self.result_word_file_name = self.result_txt_file_name.split('.')[0] + '.docx'
        self.current_directory = os.getcwd()
        self.result_directory = os.path.join(self.current_directory, 'results')
        self.result_abs_txt_file_name = os.path.join(self.result_directory, self.result_txt_file_name)
        # print(self.result_abs_txt_file_name)
        self.result_abs_word_file_name = os.path.join(self.result_directory, self.result_word_file_name)
        # print(self.result_abs_word_file_name)
        #
        self.front_door_state = OPEN
        self.back_door_state = OPEN
        #
        self.crawl_only_today = False

    def set_crawl_today(self, condition: bool):
        self.crawl_only_today = condition
        pass

    # def initiate_environment(self):
    #     if not os.path.exists(self.result_directory):
    #         os.makedirs(self.result_directory)
    #         pass
    #     pass

    def crawl_main_page_urls(self):
        urls_collection = []
        # 设置请求头，模拟正常用户的浏览器请求
        # self.headers_formed = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        #     'Accept-Language': 'en-US,en;q=0.5',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        #     'DNT': '1',  # Do Not Track 请求头
        #     'Referer': self.target_url,  # 引用页，有助于避免被识别为爬虫（有时）
        # }
        response = requests.get(self.target_url, headers=self.headers_formed)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                # 获取链接的文本和URL
                gotten_link = link.get('href')
                # print(link.get_text(), link.get('href'))
                if gotten_link in exclusion:
                    pass
                else:
                    urls_collection.append((link.get_text().strip(), gotten_link))
                    pass
                pass

            pass
        else:
            print(f"Error: {response.status_code}")
            pass
        pass
        return urls_collection

    def crawl_news_page_urls(self):
        urls_collection = []
        prefix_reg = r'(\w+\s+\d+\D+\d+\D+\d+\:\d+\s+)(?=\w+)'
        response = requests.get(self.target_url, headers=self.headers_formed)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                # 获取链接的文本和URL
                gotten_text = link.get_text().strip()
                gotten_link = link.get('href')
                clean_text = re.sub(prefix_reg, '', gotten_text, re.I | re.M)
                # dprint('>'*100)
                # dprint(clean_text)
                # dprint('<'*100)
                if gotten_link in exclusion:
                    pass
                else:
                    urls_collection.append((clean_text, gotten_link))
                    pass
                pass

            pass
        else:
            print(f"Error: {response.status_code}")
            pass
        pass
        # pprint(urls_collection)
        return urls_collection

    def record_available(self):
        if self.front_door_state == CLOSED and self.back_door_state == OPEN:
            result = True
            pass
        else:
            result = False
            pass
        return result

    def crawl_one_url_content(self, link_text, link_url, filename):
        crawl_result = True
        self.front_door_state = OPEN
        self.back_door_state = OPEN
        print('-' * 80)
        print('dealing page:', link_text)
        print('requesting link:', link_url)
        response = requests.get(link_url, headers=self.headers_formed)
        # 检查请求是否成功
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # check date
            if self.crawl_only_today:
                if date_match_today(soup):
                    dprint('notice:date matched today!')
                    pass
                else:
                    dprint('notice:date does not match today!')
                    return False
                pass
            with open(filename, mode='a+', encoding='utf-8') as file:
                for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li']):
                    if element.name in ['h1', 'h2', 'h3']:
                        file.write(element.text.strip())
                        file.write('\n\n')
                        file.flush()
                        pass
                    elif element.name == 'p':
                        file.write(element.text.strip())
                        file.write('\n')
                        file.flush()
                        pass
                    pass
                file.write('\n')
                file.flush()
                pass
            pass
        else:
            print(f"Error: {response.status_code}")
            pass
        dprint('notice,crawled the page \n{}\n successfully!'.format(link_url))
        return crawl_result

    def loop_crawl_main_page(self):
        link_text_link_url_tuple_list = self.crawl_main_page_urls()
        #
        with open(self.result_abs_txt_file_name, 'w') as file:
            file.write('')
            pass
        counter = 0
        for link_text, link_url in link_text_link_url_tuple_list:
            counter += 1
            print('\ncrawling main page number {}'.format(str(counter)))
            self.crawl_one_url_content(link_text, link_url, self.result_abs_txt_file_name)
            time.sleep(5)
            if counter >= self.crawl_number:
                break
                pass
            pass
        pass

    def loop_crawl_news_page(self):
        self.link_text_link_url_tuple_list = self.crawl_news_page_urls()
        # link_text_link_url_tuple_list = self.extract_response_title_link()
        #
        with open(self.result_abs_txt_file_name, 'w') as file:
            file.write('')
            pass
        counter = 1
        for link_text, link_url in self.link_text_link_url_tuple_list:
            print('\ncrawling news page link number {}'.format(str(counter)))
            crawl_today_successfully = self.crawl_one_url_content(link_text, link_url, self.result_abs_txt_file_name)
            time.sleep(5)
            if not crawl_today_successfully:
                continue
            WebpagePictureDownloader.download_webpage_pictures(link_url,self.picture_download_directory)
            if counter >= self.crawl_number:
                break
                pass
            counter += 1
            time.sleep(5)
            pass
        pass

    def txt2word(self):
        # 读取TXT文件内容
        with open(self.result_abs_txt_file_name, mode='r', encoding='utf-8') as file:
            text = file.read()
            pass
        # 创建一个Document对象
        doc = Document()
        # 添加文本内容到Word文档
        doc.add_paragraph(text)
        # 保存Word文档
        doc.save(self.result_abs_word_file_name)
        pass

    def run(self):
        self.initiate_environment()
        self.loop_crawl_news_page()
        self.txt2word()
        os.system('start {}'.format(self.result_directory))
        os.system('start {}'.format(self.result_abs_word_file_name))
        pass

    pass


pass


def task1():
    target_url = 'https://newsukraine.rbc.ua/news'
    referred_url = 'https://newsukraine.rbc.ua/'
    crawl_number = 15
    ins = CrawlerNewsUkraineRbcUa(target_url, None, crawl_number)
    ins.set_referred_url(referred_url)
    # ins.set_crawl_today(True)
    ins.run()
    pass


if __name__ == '__main__':
    task1()
    pass
