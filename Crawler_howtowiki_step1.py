from CrawlerBase import *


class CrawlerHowToWiki(CrawlerBase):
    def __init__(self, target_url, result_txt_file_name=None):
        super().__init__(target_url, result_txt_file_name)
        pass

    def run(self):
        response = requests.get(self.target_url, headers=self.headers_formed)
        self.extract_response_content(
            response, self.result_abs_txt_file_name, True)
        txt2word(self.result_abs_txt_file_name, self.result_abs_word_file_name)
        pass

    pass


def task1():
    url = "https://howtowiki.net/how-to-fall-asleep-tips-tricks-w-o-medication/"
    ins = CrawlerHowToWiki(url, None)
    ins.run()
    print('Finished! transforming files...\nOpening folder {} and \nfile {}'.format(
        ins.result_directory, ins.result_abs_txt_file_name))
    #
    os.system('start {}'.format(ins.result_directory))
    os.startfile(ins.result_abs_word_file_name)
    pass


if __name__ == '__main__':
    task1()
    pass
