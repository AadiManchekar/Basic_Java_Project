import json
import os
from json2html import json2html

build_number = os.environ.get('BUILD_NUMBER')
pdf_filename = f"trivy_repository_scan_{build_number}"

with open('trivy_repository_scan.json') as f:
    data = json.load(f)

html_table = json2html.convert(data)
with open(f'{pdf_filename}.html', 'w') as f:
    f.write(html_table)
