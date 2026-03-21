import sys
import json
from bs4 import BeautifulSoup

snapshot = json.load(sys.stdin)
html = snapshot.get('html', '')
soup = BeautifulSoup(html, 'html.parser')

# Find sidebar modules
sidebar_modules = soup.find_all('div', class_='sidebar-module')
subpages = []
for module in sidebar_modules:
    # Only include links with class 'item' (ignore rsslink etc.)
    for li in module.find_all('li', class_='menuItem'):
        item_link = li.find('a', class_='item', href=True)
        if item_link:
            subpages.append({
                'title': item_link.get_text(strip=True),
                'url': item_link['href'],
            })

# Main content snapshot
content_block = soup.find('div', id='content-block')
main_content = content_block.get_text(strip=True) if content_block else ''

# Find attachments (links to downloadable files)
attachments = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'downloadFile' in href:
        attachments.append({
            'filename': a.get_text(strip=True),
            'url': href,
        })

result = {
    'main_content': main_content,
    'sidebar_subpages': subpages,
    'attachments': attachments,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
