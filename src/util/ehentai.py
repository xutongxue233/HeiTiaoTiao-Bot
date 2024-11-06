import requests
from bs4 import BeautifulSoup

proxies = {
    "http": "socks5h://127.0.0.1:7890",
}

# 目标网站 URL
url = "https://e-hentai.org/"

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
                    # 将结果添加到列表
                    results.append({'href': href, 'title': title})

    else:
        print(f"请求失败，状态码：{response.status_code}")

    return results

if __name__ == "__main__":
    results = get_ehentai_list()
    # 打印结果
    for result in results:
        print(f"链接: {result['href']}, 标题: {result['title']}")