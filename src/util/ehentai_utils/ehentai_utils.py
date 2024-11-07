import requests
from bs4 import BeautifulSoup
import re

# 设置代理
proxies = {
    "http": "socks5h://127.0.0.1:7890",
}

# 目标网站 URL
url = "https://e-hentai.org/popular"


def fetch_page(url):
    """
    发起 GET 请求并返回响应的页面内容。
    :param: url (str): 目标网页的 URL。
    """
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
        return BeautifulSoup(response.text, "html.parser"), True
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None, False


def get_ehentai_list():
    """
    从 e-hentai 网站获取流行图片的列表，包括标题、链接和图片链接。
    :return: list: 包含每个项目的字典列表，字典包含 'href', 'title', 'image_url'。
    """
    results = []

    # 获取首页内容
    soup, success = fetch_page(url)
    if not success:
        return results

    # 查找所有包含图片信息的 td 标签
    td_tags = soup.find_all('td', class_='gl3c glname')
    for td in td_tags:
        a_tag = td.find('a')
        href = a_tag.get('href') if a_tag else None
        title = (lambda: td.find('div', class_='glink').get_text(strip=True) if td.find('div', class_='glink') else '无标题')()
        image_url = get_image_from_page(href) if href else None
        results.append({'href': href, 'title': title, 'image_url': image_url})

    return results


def get_image_from_page(page_url):
    """
    从单个图片页面中提取图片链接。
    :param: page_url (str): 图片页面的 URL。
    :return: str: 图片的 URL。
    """
    soup, success = fetch_page(page_url)
    if not success:
        return None

    # 查找图片链接的 div 标签
    gd1_div = soup.find('div', id='gd1')
    if gd1_div:
        nested_div = gd1_div.find('div', style=True)
        if nested_div:
            style_attr = nested_div.get('style', '')
            match = re.search(r'url\((https://[^\)]+)\)', style_attr)
            if match:
                return match.group(1)
    return None


if __name__ == "__main__":
    # 获取流行图片列表
    results = get_ehentai_list()

    # 打印结果
    if results:
        for result in results:
            print(f"链接: {result['href']}, 标题: {result['title']}, 图片链接: {result['image_url']}")
    else:
        print("没有获取到任何数据。")
