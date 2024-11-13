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
        txt2word(self.result_abs_txt_file_name,self.result_abs_word_file_name)
        pass

    pass


def task1():
    target_url = "https://www.psychologytoday.com/us/blog/liking-the-child-you-love/202411/staying-strong-when-your-adult-child-turns-mean"
    ins = CrawlerPsychologyToday(target_url)
    ins.run()

    pass


if __name__ == '__main__':
    task1()
    pass
