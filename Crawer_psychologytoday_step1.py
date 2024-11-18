from CrawlerBase import *


class CrawlerPsychologyToday(CrawlerBase):
    def __init__(self, target_url):
        super().__init__(target_url)
        self.initiate_environment()
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
    target_url = "https://www.psychologytoday.com/us/blog/modern-teen-therapy/202411/why-is-it-so-hard-for-parents-to-apologize-to-their-kids"
    ins = CrawlerPsychologyToday(target_url)
    ins.run()

    pass


if __name__ == '__main__':
    task1()
    pass
