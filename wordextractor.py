import requests
import re
import click
from bs4 import BeautifulSoup
PAGE_URL = 'https://www.nwpu.edu.cn/'
def get_html_of(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/126.0.0.0 Safari/537.36'
    }
    for attempt in range(5):
        try:
            resp = requests.get(url, headers=headers, timeout=20)
        except requests.exceptions.RequestException:
            print(f'第{attempt + 1}次尝试: 请求异常，重试...')
            continue
        if resp.status_code != 200:
            print(f'第{attempt + 1}次尝试: HTTP {resp.status_code}，重试...')
            continue
        html = resp.content.decode('utf-8', 'ignore')
        text = BeautifulSoup(html, 'html.parser').get_text()
        if len(text) > 200:
            return html
        print(f'第{attempt + 1}次尝试: 疑似校验页，重试...')
    print('多次尝试后仍未获得有效页面，请稍后重试')
    exit(1)
def password_variants(word):
    suffixes = ['2019', '1!', '2!', '3!', '01', '123']
    variants = []
    for form in (word.capitalize(), word.lower(), word.upper()):
        for suffix in suffixes:
            variants.append(form + suffix)
    return variants
@click.command()
@click.option('--url', default=PAGE_URL, help='要爬取的网址')
@click.option('--length', default=10, type=int, help='输出前N个高频词')
@click.option('--output', '-o', default=None, help='输出文件路径')
def main(url, length, output):
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    all_words = re.findall(r'\w+', raw_text)
    word_count = {}
    for word in all_words:
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    top_words = sorted(
        word_count.items(), key=lambda item: item[1], reverse=True
    )
    lines = []
    for i in range(min(length, len(top_words))):
        word = top_words[i][0]
        lines.append(word)
        lines.extend(password_variants(word))
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines) + '\n')
        print(f'已写入 {output}，共 {len(lines)} 行')
    else:
        for line in lines:
            print(line)
if __name__ == '__main__':
    main()
