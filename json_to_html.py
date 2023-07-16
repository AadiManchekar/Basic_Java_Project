import json
import os
from json2html import json2html

for filename in os.listdir('.'):
    if filename.endswith('.json'):
        json_filename = os.path.splitext(filename)[0]
        html_filename = f'{json_filename}.html'
        
        with open(filename) as json_file:
            data = json.load(json_file)
            
        html_table = json2html.convert(data)
        
        with open(html_filename, 'w') as html_file:
            html_file.write(html_table)
