import sys
import json
from bs4 import BeautifulSoup

# Read JSON snapshot from stdin
snapshot = json.load(sys.stdin)
html = snapshot.get('html', '')

soup = BeautifulSoup(html, 'html.parser')
# Find the table with class 'scplan table'
table = soup.find('table', class_='scplan table')
if not table:
    print('No scplan table found.')
    sys.exit(1)

subjects = []
current_group = []
group_stack = []

for row in table.find_all('tr'):
    row_class = row.get('class', [])
    if 'scplangroup' in row_class:
        # New group, update stack
        group_text = row.find('td', class_='scplancolcurricularcourse')
        if group_text:
            group_name = group_text.get_text(strip=True)
            group_stack.append(group_name)
    elif 'scplandismissal' in row_class or 'scplanenrollment' in row_class:
        # Subject row
        subject = {}
        subject['groups'] = list(group_stack)
        course_cell = row.find('td', class_='scplancolcurricularcourse')
        if course_cell:
            link = course_cell.find('a')
            subject['name'] = link.get_text(strip=True) if link else course_cell.get_text(strip=True)
            subject['url'] = link['href'] if link and link.has_attr('href') else None
        subject['grade'] = row.find('td', class_='scplancolgrade').get_text(strip=True) if row.find('td', class_='scplancolgrade') else None
        subject['ects'] = row.find('td', class_='scplancolects').get_text(strip=True) if row.find('td', class_='scplancolects') else None
        subject['year'] = row.find('td', class_='scplancolyear').get_text(strip=True) if row.find('td', class_='scplancolyear') else None
        subject['semester'] = row.find('td', class_='scplancolsemester').get_text(strip=True) if row.find('td', class_='scplancolsemester') else None
        subjects.append(subject)
    # Remove group from stack if next row is not indented
    if 'scplangroup' in row_class and not row.find('td', class_='scplancolident'):
        group_stack = []

if not subjects:
    print('No subjects found.')
    sys.exit(1)

print(json.dumps(subjects, indent=2, ensure_ascii=False))
