import sys
import json
from bs4 import BeautifulSoup

# Read JSON snapshot from stdin
snapshot = json.load(sys.stdin)
html = snapshot.get('html', '')

soup = BeautifulSoup(html, 'html.parser')
content = soup.find(id='content-block')
if not content:
    print('No content-block found.')
    sys.exit(1)

# Find the heading for Registrations or Matrículas
heading = None
for tag in content.find_all(['h2', 'h3', 'h4']):
    if tag.get_text(strip=True).lower() in ['registrations', 'matrículas', 'matriculas']:
        heading = tag
        break
if not heading:
    print('No "Registrations" heading found.')
    sys.exit(1)

# The table should be immediately after the heading
table = heading.find_next('table')
if not table:
    print('No table found after Registrations heading.')
    sys.exit(1)

courses = []
for row in table.find_all('tr')[1:]:  # skip header
    cells = row.find_all('td')
    if not cells:
        continue
    # Try to extract course name and link
    link = cells[0].find('a')
    course_name = link.get_text(strip=True) if link else cells[0].get_text(strip=True)
    plan_url = link['href'] if link and link.has_attr('href') else None
    degree = cells[1].get_text(strip=True) if len(cells) > 1 else ''
    year = cells[2].get_text(strip=True) if len(cells) > 2 else ''
    courses.append({
        'course_name': course_name,
        'degree': degree,
        'year': year,
        'plan_url': plan_url,
    })

if not courses:
    print('No courses found.')
    sys.exit(1)

print(json.dumps(courses, indent=2, ensure_ascii=False))
