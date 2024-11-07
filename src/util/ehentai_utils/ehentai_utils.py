import requests
from bs4 import BeautifulSoup

proxies = {
    "http": "socks5h://127.0.0.1:7890",  # 使用代理
}

# 目标网站 URL
url = "https://e-hentai.org/popular"


def get_ehentai_list(max_results=5):
    # 爬取的结果
    results = []
    count = 0  # 计数器

    # 发起请求
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # 如果响应码不是 200，将引发异常

        # 如果请求成功，解析页面内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 查找目标 table（class 为 'itg gltc'）
        table = soup.find('table', class_='itg gltc')
        if table:
            # 查找所有包含信息的 tr 标签
            tr_tags = table.find_all('tr')

            for tr in tr_tags:
                if count >= max_results:
                    break  # 达到最大爬取数量，跳出循环

                # 查找包含图片链接的 td 标签（class 为 'gl2c'，里面有 glthumb）
                td_thumb = tr.find('td', class_='gl2c')
                if td_thumb:
                    # 在 td_thumb 中查找 glthumb 的 div 标签，并获取 img 标签
                    div_thumb = td_thumb.find('div', class_='glthumb')
                    if div_thumb:
                        img_tag = div_thumb.find('img')
                        if img_tag:
                            # 检查 img 标签的 src 是否为 base64 编码的链接
                            image_url = img_tag.get('src')
                            if image_url.startswith('data:image'):
                                # 如果是 base64 编码的数据，尝试获取 data-src
                                image_url = img_tag.get('data-src')
                        else:
                            image_url = None
                    else:
                        image_url = None
                else:
                    image_url = None

                # 查找 td 标签中包含标题的部分（class 为 'gl3c glname'）及其子 div class='glink'
                td_name = tr.find('td', class_='gl3c glname')
                if td_name:
                    div_glink = td_name.find('div', class_='glink')
                    if div_glink:
                        title = div_glink.get_text(strip=True)
                    else:
                        title = None

                    # 查找详情 URL（在 td_name 中的 a 标签）
                    a_tag = td_name.find('a')
                    if a_tag:
                        href = a_tag.get('href')
                    else:
                        href = None

                    # 查找页数信息（在 class 为 'gl4c glhide' 的 td 中）
                    td_pages = tr.find('td', class_='gl4c glhide')
                    if td_pages:
                        div_pages = td_pages.find_all('div')
                        if div_pages:
                            pages_text = div_pages[-1].get_text(strip=True)  # 获取最后一个 div 中的文本
                            pages = pages_text.split()[0]  # 提取数字部分
                        else:
                            pages = None
                    else:
                        pages = None

                    # 将结果添加到列表，包括标题、链接、图片链接和页数
                    results.append({
                        'href': href,
                        'title': title,
                        'image_url': image_url,
                        'pages': pages
                    })
                    count += 1  # 成功添加一条记录后，计数器加 1

    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")

    return results


if __name__ == "__main__":
    results = get_ehentai_list(max_results=10)
    # 打印结果
    for result in results:
        print(f"链接: {result['href']}, 标题: {result['title']}, 图片链接: {result['image_url']}, 页数: {result['pages']}")
