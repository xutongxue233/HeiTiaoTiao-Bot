import requests
from bs4 import BeautifulSoup
import re

proxies = {
    "http": "socks5h://127.0.0.1:7890",
}

# 目标网站 URL
url = "https://e-hentai.org/popular"


def get_ehentai_list():
    # 爬取的结果
    results = []

    # 发起请求
    response = requests.get(url, proxies=proxies)

    # 如果请求成功，解析页面内容
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # 查找所有 class 为 'gl3c glname' 的 td 标签
        td_tags = soup.find_all('td', class_='gl3c glname')
        for td in td_tags:
            # 获取 td 中 a 标签的 href 属性
            a_tag = td.find('a')
            if a_tag:
                href = a_tag.get('href')
                # 获取 class 为 'glink' 的标题
                glink_tag = td.find('div', class_='glink')
                if glink_tag:
                    title = glink_tag.get_text()
                    # 获取每个页面中的图片链接
                    image_url = get_image_from_page(href)
                    # 将结果添加到列表，包括标题、链接和图片链接
                    results.append({'href': href, 'title': title, 'image_url': image_url})

    else:
        print(f"请求失败，状态码：{response.status_code}")

    return results


def get_image_from_page(page_url):
    # 获取每个页面中的图片链接
    image_url = None
    page_response = requests.get(page_url, proxies=proxies)

    if page_response.status_code == 200:
        page_soup = BeautifulSoup(page_response.text, "html.parser")
        # 查找 id 为 'gd1' 的 div 标签
        gd1_div = page_soup.find('div', id='gd1')
        if gd1_div:
            # 查找嵌套在 id="gd1" 下的 div 标签
            nested_div = gd1_div.find('div', style=True)
            if nested_div:
                # 获取 style 属性中的背景图片 URL
                style_attr = nested_div.get('style')
                if style_attr:
                    # 使用正则表达式提取图片 URL
                    match = re.search(r'url\((https://[^\)]+)\)', style_attr)
                    if match:
                        image_url = match.group(1)
    else:
        print(f"请求失败，状态码：{page_response.status_code}")

    return image_url


if __name__ == "__main__":
    results = get_ehentai_list()
    # 打印结果
    for result in results:
        print(f"链接: {result['href']}, 标题: {result['title']}, 图片链接: {result['image_url']}")