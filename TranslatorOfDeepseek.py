from CrawlerBase import get_deepseek_translation


def translate_file_to_file(source, destination):
    prompt = (
        "with the following rules:"
        "Rule 1: translate and remove all supplementary explanations, postscripts, editorial notes, tip,hint which are commonly provided by system within parentheses."
        "translate the following content into Simplified Chinese:")
    paragraphs = open(source, encoding='utf-8', mode='r').readlines()
    for one_line in paragraphs:
        question = prompt + one_line
        print('sending to deepseek:', question)
        translated_paragraph = get_deepseek_translation(question)
        print('deepseek answer:\n', translated_paragraph)
        print('\n\n')
        # write txt file
        with open(destination, mode='a+', encoding='utf-8') as output_file:
            output_file.write('\n')
            output_file.write(translated_paragraph)
            output_file.flush()
            pass
        pass
    pass


def task1():
    source = r"G:\MineLess\Python\projects\bwcrawler\news_ukraine_text_files_2025-05-24\othernews1.txt"
    destination = r"G:\MineLess\Python\projects\bwcrawler\news_ukraine_text_files_2025-05-24\othernews1_translation.txt"
    translate_file_to_file(source, destination)
    pass


def task2():
    destination = r"G:\MineLess\Python\projects\bwcrawler\news_ukraine_text_files_2025-05-24\othernews_translation.txt"
    dest_folder = 'G:\MineLess\Python\projects\bwcrawler\news_ukraine_text_files_'
    dest_file = 'othersnews.txt'
    lines = open(destination, encoding='utf-8', mode='r').readlines()
    # print(lines)
    for line in lines:
        if line.endswith(':'):
            continue
            pass
        if "目标内容如下：" in line:
            continue
        print(line)
        pass
    pass


if __name__ == '__main__':
    task1()
    pass
