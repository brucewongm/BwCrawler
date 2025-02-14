from http.cookiejar import reach

from PIL import Image
from io import BytesIO
from CrawlerBase import *
from CrawlerBaseExclusion import *

exclusion = """https://newsukraine.rbc.ua/
ua https://www.rbc.ua/
https://newsukraine.rbc.ua/about.shtml
https://newsukraine.rbc.ua/termsofuse.shtml
https://newsukraine.rbc.ua/legacy.shtml
https://newsukraine.rbc.ua/static/principles/index.html
https://newsukraine.rbc.ua/privacypolicy.shtml
https://newsukraine.rbc.ua/contacts.shtml
https://newsukraine.rbc.ua/becomeauthor.shtml
https://newsukraine.rbc.ua/static/principles/index.html
https://newsukraine.rbc.ua/static/command/index.html
x https://x.com/NewsUkraineRBC
en javascript:;
https://whatsapp.com/channel/0029VaVYmRP0rGiPdNM12L2g
https://newsukraine.rbc.ua/search
https://twitter.com/NewsUkraineRBC
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
news_ukraine_keyword = "https://newsukraine.rbc.ua/news"
OPEN = 1
CLOSED = 0
TIME_INTERVAL_OF_WEBPAGES = 6
TIME_INTERVAL_OF_PICTURES = 3


class CrawlerNewsUkraineRbcUaNewsPage(CrawlerBase):
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

    def crawl_news_page_urls_old(self):
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
                    continue
                elif news_ukraine_keyword not in gotten_link:
                    continue
                else:
                    pass
                urls_collection.append((clean_text, gotten_link))

                pass

            pass
        else:
            print(f"Error: {response.status_code}")
            pass
        pass
        print('urls_collection:')
        pprint(urls_collection)
        crawled_url_number = len(urls_collection)
        print('the number of crawled url links is {}'.format(str(crawled_url_number)))
        while True:
            cmd = input("verify the crawled urls ,are you sure to go on crawling ?(Y/N):")
            if not cmd:
                continue
            elif cmd.lower() == 'y':
                break
            elif cmd.lower() == 'n':
                continue
                # exit(0)
                pass
            pass
        return urls_collection

    def crawl_news_page_urls(self):
        print("Crawling news page urls...")
        prefix_reg = r'(\w+\s+\d+\D+\d+\D+\d+\:\d+\s+)(?=\w+)'
        reach_flag = True
        urls_collection = []
        while reach_flag:
            urls_collection = []
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
                        continue
                    elif news_ukraine_keyword not in gotten_link:
                        continue
                    else:
                        pass
                    urls_collection.append((clean_text, gotten_link))

                    pass

                pass
            else:
                print(f"Error: {response.status_code}")
                pass
            pass
            print('urls_collection:')
            # pprint(urls_collection)
            # print('the number of crawled url links is {}'.format(str(len(urls_collection))))
            crawled_url_number = len(urls_collection)
            print('the number of crawled url links is {}'.format(str(crawled_url_number)))
            # while True:
            #     cmd = input("verify the number crawled urls ,are you sure to go on crawling ?(Y/N):")
            #     if cmd.lower() == 'y':
            #         reach_flag = False
            #         break
            #         pass
            #     elif cmd.lower() == 'n':
            #         break
            #         pass
            #     else:
            #         continue
            #         pass
            #     pass
            if crawled_url_number >= 30:
                break
            response = None
            pause(6)
            pass
        return urls_collection

    def crawl_one_url_content(self, link_text, link_url, filename):
        crawl_result = True
        self.front_door_state = OPEN
        self.back_door_state = OPEN
        print('-' * 80)
        print('dealing page:', link_text)
        print('requesting link:', link_url)
        response = requests.get(link_url, headers=self.headers_formed)
        # 检查请求是否成功
        try:
            print("response.status_code:", response.status_code)
            pass
        except:
            pass
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
                file.write('\ntitle:\n')
                # file.write(link_text)
                file.write('\n')
                file.flush()
                for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li']):
                    if element.name in ['h1', 'h2', 'h3']:
                        file.write(element.text.strip())
                        file.write('\n')
                        file.flush()
                        pass
                    elif element.name == 'p':
                        file.write(element.text.strip())
                        file.write('\n')
                        file.flush()
                        pass
                    pass
                file.write('\n\n')
                file.flush()
                pass
            pass
        else:
            print(f"Error: {response.status_code}")
            crawl_result = False
            pass
        dprint('notice,crawled the page \n{}\nsuccessfully!'.format(link_url))
        return crawl_result

    def loop_crawl_news_page(self):
        self.link_text_link_url_tuple_list = self.crawl_news_page_urls()
        # link_text_link_url_tuple_list = self.extract_response_title_link()
        #
        with open(self.result_abs_txt_file_name, 'w') as file:
            file.write('\ntitle:\n')
            pass
        loop_counter = 1
        for link_text, link_url in self.link_text_link_url_tuple_list:
            print('\nThis page sequence number is {}'.format(str(loop_counter)))
            if link_url in self.finished_url_list:
                print('{}\nis already in finished url list.'.format(link_url))
                self.logger.debug('found ({}) in finished record.'.format(link_url))
                loop_counter += 1
                self.logger.debug('counter add 1 to be {}.'.format(str(loop_counter)))
                if loop_counter > self.crawl_number:
                    print('Target crawl number reached!')
                    break
                    pass
                continue
            print('\ncrawling news page link number {}/{}'.format(str(loop_counter), str(self.crawl_number)))
            self.logger.debug('start crawling ({}).'.format(link_url))
            crawl_this_successfully = self.crawl_one_url_content(link_text, link_url, self.result_abs_txt_file_name)
            self.logger.debug('this crawl result:{}'.format(str(crawl_this_successfully)))
            count_down_seconds(TIME_INTERVAL_OF_WEBPAGES)
            if not crawl_this_successfully:
                continue
            # WebpagePictureDownloader.download_webpage_pictures(link_url, self.picture_download_directory)
            print('Starting crawling pictures...')
            WebpagePictureDownloader.download_webpage_pictures_of_the_size(link_url,
                                                                           save_folder=self.picture_download_directory)
            pass
            self.finished_url_list.append(link_url)
            finished_urls_text = '\n'.join(self.finished_url_list)
            with open(self.finished_target_url_log_file, mode='w+', encoding='utf-8') as f:
                f.write(finished_urls_text)
                f.flush()
                pass
            self.logger.debug('crawl page ({}) and write record successfully.'.format(link_url))
            loop_counter += 1
            self.logger.debug('counter add 1 to be {}.'.format(str(loop_counter)))
            if loop_counter > self.crawl_number:
                print('Target crawl number reached!')
                break
                pass
            count_down_seconds(TIME_INTERVAL_OF_WEBPAGES)
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
    crawl_number = 30
    ins = CrawlerNewsUkraineRbcUaNewsPage(target_url, None, crawl_number)
    ins.set_referred_url(referred_url)
    # ins.set_crawl_today(True)
    ins.run()
    input('finished crawling,input any string to exit:')
    pass


def task2():
    url_list = [
        "https://newsukraine.rbc.ua/static/img/_/t/_tramp_ze_4ce362f2a56fc0da5690a0e52f024de5_1300x820_7d46981567ab4506ec093426c0b48a28_260x164.jpg",
        "https://newsukraine.rbc.ua/static/img/_/t/_tramp_ze_4ce362f2a56fc0da5690a0e52f024de5_1300x820_7d46981567ab4506ec093426c0b48a28_650x410.jpg"
    ]

    # 使用requests下载图片
    for url in url_list:
        response = requests.get(url)
        print('mark')
        # 检查请求是否成功
        if response.status_code == 200:
            # 将图片内容载入到BytesIO中
            image = Image.open(BytesIO(response.content))
            # 获取图片的宽度和高度
            width, height = image.size
            print(f'图片宽度: {width}, 图片高度: {height}')
        else:
            print('图片下载失败')
        pass
        # sleep(3)
        count_down_seconds(TIME_INTERVAL_OF_PICTURES)
        pass
    pass


pass
if __name__ == '__main__':
    task1()
pass
