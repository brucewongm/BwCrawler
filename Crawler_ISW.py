import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import chardet
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from CrawlerBase import *

class ISWScraper:
    def __init__(self, base_url="https://understandingwar.org",
                 image_dir="isw_downloaded_images_"+moment()):
        self.base_url = base_url
        self.image_dir = image_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self._setup_directories()

    def _setup_directories(self):
        """创建必要的目录"""
        os.makedirs(self.image_dir, exist_ok=True)

    def download_image(self, url):
        """下载单张图片"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = os.path.basename(url.split('?')[0])
            save_path = os.path.join(self.image_dir, filename)

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"下载成功: {filename}")
            return True
        except Exception as e:
            print(f"下载失败 {url}: {e}")
            return False

    def download_pdf(self, pdf_link):
        """下载PDF文件"""
        try:
            response = requests.get(pdf_link, stream=True)
            response.raise_for_status()

            filename = os.path.basename(pdf_link)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"PDF文件已成功下载到: {os.path.abspath(filename)}")
            return True
        except Exception as e:
            print(f"下载PDF时出错: {e}")
            return False

    def _extract_metadata(self, soup):
        """提取文章元数据"""
        title = soup.find('h1', {'id': 'page-title'}).get_text(strip=True)
        submitted = soup.find('span', class_='submitted').get_text(strip=True)

        print("Title:", title)
        print("Publication Info:", submitted)

        return {
            'title': title,
            'submitted': submitted
        }

    def _extract_main_content(self, soup):
        """提取正文内容"""
        content_div = soup.find('div', class_='field-name-body')
        if not content_div:
            print("Could not find main content")
            return None

        paragraphs = [p.get_text(strip=True) for p in content_div.find_all('p')]
        main_content = '\n'.join(paragraphs)

        print("\nMain Content:")
        print(main_content)

        return main_content

    def _extract_pdf_link(self, soup):
        """提取PDF链接"""
        pdf_div = soup.find('div', class_='field-name-field-pdf-report')
        if not pdf_div:
            return None

        pdf_link = pdf_div.find('a')['href']
        if not pdf_link.startswith('http'):
            pdf_link = urljoin(self.base_url, pdf_link)

        print("\nPDF Link:", pdf_link)
        return pdf_link

    def _extract_and_download_images(self, soup):
        """提取并下载图片"""
        content_div = soup.find('div', class_='field-name-body')
        if not content_div:
            print("未找到正文内容")
            return []

        images = content_div.find_all('img')
        print(f"找到 {len(images)} 张图片")

        image_urls = []
        for img in images:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                img_url = urljoin(self.base_url, img_url)

            # 只下载特定类型的图片
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not any(img_url.lower().endswith(ext) for ext in valid_extensions):
                continue

            image_urls.append(img_url)
            pass

        print('开始多线程下载图片...')
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.download_image, image_urls)

        return image_urls

    def scrape_article(self, url, download_images=True, download_pdf=True):
        """主方法：抓取文章内容"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            # 检测编码
            detected_encoding = chardet.detect(response.content)['encoding']
            print(f"Detected encoding: {detected_encoding}")

            soup = BeautifulSoup(
                response.content,
                'html.parser',
                from_encoding=detected_encoding)

            # 提取各种信息
            metadata = self._extract_metadata(soup)
            content = self._extract_main_content(soup)
            pdf_link = self._extract_pdf_link(soup)

            if download_pdf and pdf_link:
                self.download_pdf(pdf_link)

            if download_images:
                self._extract_and_download_images(soup)

            print('-' * 80)

            return {
                'metadata': metadata,
                'content': content,
                'pdf_link': pdf_link
            }

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    scraper = ISWScraper()

    # 示例URL
    url = "https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment-april-28-2025/"

    # 抓取文章
    result = scraper.scrape_article(url)

    # 也可以单独下载PDF
    # pdf_link = "https://understandingwar.org/sites/default/files/2025-04-28-PDF-Russian%20Offensive%20Campaign%20Assessment.pdf"
    # scraper.download_pdf(pdf_link)