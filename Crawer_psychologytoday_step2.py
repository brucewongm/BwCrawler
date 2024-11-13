from CrawlerBase import *


class CrawlerPsychologyToday(CrawlerBase):
    def __init__(self, target_url):
        super().__init__(target_url)
        self.set_referred_url("https://www.psychologytoday.com/us")
        pass

    def run(self):
        response = requests.get(self.target_url, headers=self.headers_formed)
        self.extract_response_content(
            response, self.result_abs_txt_file_name, True)
        txt2word(self.result_abs_txt_file_name, self.result_abs_word_file_name)
        pass

    pass


def task1():
    target_url = "https://www.psychologytoday.com/us/blog/the-asymmetric-brain/202411/unmarried-people-have-a-higher-risk-of-depression"
    ins = CrawlerPsychologyToday(target_url)
    ins.run()

    pass


def task2():
    compose_english_chinese_doc_files()
    pass


if __name__ == '__main__':
    DebugSwitch += 0
    task2()
    pass
