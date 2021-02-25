from bs4 import BeautifulSoup
from collections import deque
import re
import os


def build_tree(path):
    files = dict().fromkeys(os.listdir(path))
    exp = re.compile(r"(?<=/wiki/)[\w()]+")

    for file in files:
        files[file] = []

        try:
            with open(path + file, encoding='utf-8') as code:
                links = set(exp.findall(code.read()))
        except FileNotFoundError:
            links = None

        for link in links:
            if (link in files.keys()) and (link != file) and (link not in files[file]):
                files[file].append(link)

    return files


def build_bridge(path, start_page, end_page):
    pages = build_tree(path)

    parents = {start_page: None}
    queue = deque([start_page])

    while queue:
        cur_page = queue.popleft()

        if cur_page == end_page:
            break

        for page in pages.get(cur_page):
            if page not in parents.keys():
                parents.update({page: cur_page})
                queue.append(page)

    parent = parents.get(end_page)
    result = [end_page]

    while parent:
        result.append(parent)
        parent = parents.get(parent)

    result.reverse()

    return result


def get_statistics(path, start_page, end_page):
    pages = build_bridge(path, start_page, end_page)
    pages.reverse()
    statistic = dict()

    for page in pages:
        statistic.update({page: parse(path + page)})

    return statistic


def parse(path_to_file):
    imgs = 0
    headers = 0
    linkslen = 0
    lists = 0

    page = open(path_to_file, 'r', encoding='utf-8')
    soup = BeautifulSoup(page, 'lxml').find('div', id="bodyContent")

    for tag in soup.find_all('img'):
        if int(tag.get('width') or 0) >= 200:
            imgs += 1

    all_h = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    for tag in soup.find_all(all_h):
        if tag.text[0] in ['C', 'T', 'E']:
            headers += 1

    ol_ul = ['ol', 'ul']

    for tag in soup.find_all('a'):
        tmp = 1

        for element in tag.find_next_siblings():
            if element.name == 'a':
                tmp += 1
            elif element.name is None or element.name == 'br':
                continue
            else:
                break

        if tmp > linkslen:
            linkslen = tmp

    for tag in soup.find_all(ol_ul):
        tmp = 1

        for parent in tag.parents:
            if parent.name == 'li':
                tmp = 0
                break

        lists += tmp

    page.close()

    return [imgs, headers, linkslen, lists]
