import os
import requests
from bs4 import BeautifulSoup
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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

# 获取页面的标题，去除可能导致文件路径问题的符号
def get_title(page_url):
    html = fetch_page(page_url)
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('h1', {'id': 'gj'})
    title = title_tag.get_text(strip=True) if title_tag else 'unknown_title'

    # 去除文件路径不合法的字符
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

# 创建 PDF 并插入图片，使用 reportlab 支持 webp 格式
def create_pdf_from_images(images, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    for img_path in images:
        if not img_path:
            continue  # 如果图片下载失败，跳过该图片

        try:
            c.drawImage(img_path, 10, 500, width=500, height=500)  # 这里插入图片，调整大小
            c.showPage()  # 生成新的一页
        except Exception as e:
            print(f"Error adding image {img_path} to PDF: {e}")
            continue  # 跳过添加失败的图片

    c.save()
    return pdf_path  # 返回生成的 PDF 文件路径

def download_images_and_create_pdf(url, pic_num, max_threads=5):
    title = get_title(url)
    folder_path = os.path.join(base_folder, title)

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

    # 创建 PDF
    pdf_path = os.path.join(base_folder, f"{title}.pdf")
    pdf_path = create_pdf_from_images(image_paths, pdf_path)

    return pdf_path  # 返回 PDF 文件路径

# 调用函数
# file_path = download_images_and_create_pdf('https://e-hentai.org/g/3115032/765c30fc9c/', 18, max_threads=10)
# print(f"PDF generated at: {file_path}")
