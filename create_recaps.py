import yaml
import os
import sys
import argparse
import re
from PIL import Image

def print_head():
    print('''<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recapy Komiedii Lochowej</title>
        <link href="style.css" rel="stylesheet" type="text/css" media="all">
        <script src="show.js"></script>
    </head>''')

def format_paragraphs(description):
    return re.sub(r"\n", r"\n</p><p>", description, flags=re.MULTILINE)

def read_in_file(filepath, gm):
    with open(filepath, 'r') as file:
        raw_text = file.read()
        if gm:
            raw_text = re.sub(r'<<',"<i>",raw_text)
            raw_text = re.sub(r'>>',"</i>",raw_text)
        else:
            raw_text = re.sub(r'<<.+?>>',"",raw_text, flags=re.MULTILINE)
    return raw_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description ='Create recaps.html file')
    parser.add_argument('-g', dest ='gm', action ='store_true', help ='gm output')
    args = parser.parse_args()
    factions_total = {}

    print_head()
    print("<body>")
    print('<div class="wrapper">')
    try:
        recaps = yaml.safe_load(read_in_file(f'recaps.yaml', args.gm))
        for recap in recaps:
            print('<div class="recapbox">')
            print(f'<h4>{recap['date']} : {recap['title']}</h4>')
            print('<p>')
            print(format_paragraphs(recap['desc']))
            print('</p>')
            print('</div>')
    except:
        pass

    print('</div>')
    print("</body>")
    print("</html>")
