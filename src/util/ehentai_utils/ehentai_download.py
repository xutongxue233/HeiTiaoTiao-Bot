import os
import uuid

import requests
from PIL import Image
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

# 设置下载图片的基本目录
base_folder = os.path.join(os.getcwd(), 'data', 'ehentai')
if not os.path.exists(base_folder):
    os.makedirs(base_folder)


# 获取页面内容
def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def get_title(page_url):
    html = fetch_page(page_url)
    soup = BeautifulSoup(html, 'html.parser')
    # 尝试获取 id 为 'gj' 的标题
    title_tag = soup.find('h1', {'id': 'gj'})
    # 如果为空，尝试获取 id 为 'gn' 的标题
    if not title_tag.get_text(strip=True):
        title_tag = soup.find('h1', {'id': 'gn'})
    # 获取标题文本
    title = title_tag.get_text(strip=True) if title_tag else 'unknown_title'
    print("title: " + title)
    # 如果标题为空，生成随机字符串
    if not title or title == 'unknown_title':
        title = str(uuid.uuid4())  # 生成随机字符串
    # 去除不允许的字符
    title = re.sub(r'[\/:*?"<>|]', '_', title)
    return title


# 获取每页的所有 a 标签链接
def get_page_links(page_url):
    html = fetch_page(page_url)
    soup = BeautifulSoup(html, 'html.parser')

    gdt_div = soup.find('div', {'id': 'gdt'})
    a_tags = gdt_div.find_all('a') if gdt_div else []
    page_links = []

    for a_tag in a_tags:
        href = a_tag.get('href')
        if href:
            page_links.append(href)

    return page_links


# 获取图片页面的实际图片 URL
def get_image_url(image_page_url):
    html = fetch_page(image_page_url)
    soup = BeautifulSoup(html, 'html.parser')
    img_tag = soup.find('img', {'id': 'img'})
    img_url = img_tag.get('src') if img_tag else None
    return img_url


# 下载并保存图片
def download_image(img_url, img_path):
    try:
        # 判断图片是否已经下载过
        if os.path.exists(img_path):
            print(f"Image {img_path} already exists. Skipping download.")
            return img_path  # 如果文件已存在，直接返回文件路径

        # 下载图片
        img_data = requests.get(img_url).content
        if not img_data:
            print(f"Warning: Failed to download image {img_url}. Skipping.")
            return None  # 跳过当前图片

        with open(img_path, 'wb') as f:
            f.write(img_data)

        return img_path  # 返回图片文件路径

    except Exception as e:
        print(f"Error with image {img_url}: {e}")
        return None  # 下载或处理失败时返回 None


# 将所有图片合成一张长图
def create_long_image(images, output_path):
    # 判断长图是否已经存在
    if os.path.exists(output_path):
        print(f"Long image {output_path} already exists. Returning existing file.")
        return output_path  # 如果长图已存在，直接返回

    # 计算拼接后的长图尺寸
    total_height = 0
    max_width = 0
    image_objects = []

    # 读取所有图片，计算宽度和总高度
    for img_path in images:
        try:
            img = Image.open(img_path)
            img_width, img_height = img.size
            total_height += img_height  # 累加总高度
            max_width = max(max_width, img_width)  # 获取最大的宽度
            image_objects.append(img)
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")

    # 创建一个新的空白图像，用于拼接
    long_image = Image.new('RGB', (max_width, total_height))

    # 拼接图片
    current_height = 0
    for img in image_objects:
        long_image.paste(img, (0, current_height))
        current_height += img.height  # 更新当前的拼接位置

    # 保存长图
    long_image.save(output_path)
    return output_path  # 返回长图文件路径


# 下载图片并拼接为长图
def download_images_and_create_long_image(url, pic_num, max_threads=5):
    print("图片：" + url + "  图片数量:" + str(pic_num))
    title = get_title(url)
    folder_path = os.path.join(base_folder, title)

    # 确保使用正斜杠或者反斜杠（Windows兼容）
    folder_path = os.path.normpath(folder_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    total_images = pic_num
    total_pages = total_images // 20 + (1 if total_images % 20 != 0 else 0)

    image_paths = []
    image_counter = 1

    # 使用线程池进行多线程下载
    with ThreadPoolExecutor(max_threads) as executor:
        futures = []

        for page in range(total_pages):
            page_url = f"{url}?p={page}"
            page_links = get_page_links(page_url)

            for link in page_links:
                img_url = get_image_url(link)
                if img_url:
                    img_name = f"{image_counter}.webp"  # 使用 webp 扩展名
                    img_path = os.path.join(folder_path, img_name)

                    # 提交下载任务到线程池
                    future = executor.submit(download_image, img_url, img_path)
                    futures.append(future)

                    image_counter += 1

        # 等待所有任务完成
        for future in futures:
            downloaded_img_path = future.result()
            if downloaded_img_path:  # 如果下载成功，才添加到路径列表
                image_paths.append(downloaded_img_path)

    # 拼接图片并保存为长图
    long_image_path = os.path.join(folder_path, f'{title}.jpg')  # 使用 title 作为文件名
    return create_long_image(image_paths, long_image_path)  # 返回长图文件路径

# 调用函数示例
# long_image_path = download_images_and_create_long_image('https://e-hentai.org/g/3115875/8cce20227a/', 20, max_threads=10)
# print(f"Long image generated at: {long_image_path}")

# long_image_path = download_images_and_create_long_image('https://e-hentai.org/g/3115032/765c30fc9c/', 18, max_threads=10)
# print(f"Long image generated at: {long_image_path}")
