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
        <title>Shadowrun w domu</title>
        <link href="style.css" rel="stylesheet" type="text/css" media="all">
        <script src="show.js"></script>
    </head>''')

def format_paragraphs(description):
    return re.sub(r"\n", r"\n</p><p>", description, flags=re.MULTILINE)

def print_faction_entry(data, gm, faction):
    print(f'    <li><h4 class="factionlink" onclick="toggleDisplay(\'{faction}\')"><img class="logo" src="logos/{data["logo"]}"> {data["name"]}: {data["tier"]} {data["hold"]}, status: {data["status"]} </h4>')
    print(f'         <div class="factionbox" id="{faction}" style="display:none">')
    print(f'<img src="pics/{data["hq"]["img"]}" class="hqpic"/> <p>{format_paragraphs(data["description"])}</p><h5>Miejsce</h5><p>{format_paragraphs(data["hq"]["desc"])} </p>')

    print('<h5>Szychy</h5><ul>')
    for npc in data["npcs"]:
        if "img" in npc:
            print(f'<li class="npc">{npc["name"]}: {npc["desc"]}<span><img src="pics/{npc["img"]}"></span></li>')
        else:
            print(f'<li>{npc["name"]}: {npc["desc"]}</li>')
    print('</ul>')

    if list(filter(None, data["assets"])):
        print('<h5>Zasoby</h5><ul>')
        for asset in filter(None, data["assets"]):
            print(f'<li class="asset">{asset}</li>')
        print('</ul>')

    print('<h5>Sojusznicy i rywale</h5><ul>')
    for friend in data["friends"]:
        print(f'<li class="friend">{friend}</li>')
    for enemy in data["enemies"]:
        print(f'<li class="enemy">{enemy}</li>')

    print('</ul><h5>Zegarki</h5>')
    for clock in data["clocks"]:
        print(f'<p><span class="clock"><img class="clock" src="staticimgs/clock/{clock["size"]}-{clock["filled"]}.png"> {clock["desc"]}</span></p>')
    print("         </div>")
    print("    </li>")

def read_in_file(filepath, gm):
    with open(filepath, 'r') as file:
        raw_text = file.read()
        if gm:
            raw_text = re.sub(r'<<',"<i>",raw_text)
            raw_text = re.sub(r'>>',"</i>",raw_text)
        else:
            raw_text = re.sub(r'<<.+?>>',"",raw_text, flags=re.MULTILINE)
    return raw_text

def create_image(image_base_name, factions):
    with Image.open(f'berlin-{image_base_name}.png') as mapimage:
        for faction in factions:
            if 'location' in factions[faction]['hq'] and image_base_name in factions[faction]['hq']['location'] and 'logo' in factions[faction]:
                logo_image = Image.open(f'generated_files/logos/{factions[faction]["logo"]}')
                logo_image = logo_image.resize((50,50))
                for coords in factions[faction]['hq']['location'][image_base_name]:
                    mapimage.paste(logo_image, tuple(coords), logo_image)

        mapimage.save(f'generated_files/maps/berlin-{image_base_name}.jpg')

tier_to_num = {"I": 9, "II": 8, "III": 7, "IV": 6, "V": 5, "VI": 4, "VII": 3, "VIII": 2}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description ='Create index.html file')
    parser.add_argument('-g', dest ='gm', action ='store_true', help ='gm output')
    args = parser.parse_args()
    factions_total = {}

    print_head()
    print("<body>")
    print('<div class="wrapper">')
    print(f"<h1>Gracze</h1>")
    print(f"<h1>Materiały</h1>")
    print(f'<img src="staticimgs/under_construction.gif">')
    print(f'<a href="construction.html">Recapy</a></h1>')
    print(f'<a href="construction.html">Mapki</a></h1>')
    print(f"<h1>Frakcje</h1>")
    for type in os.listdir("factions"):
        factions = {}
        print(f"<h2>{type}:</h2>")
        print("<ul>")
        for faction in sorted(os.listdir(f"factions/{type}")):
            factions[faction] = yaml.safe_load(read_in_file(f'factions/{type}/{faction}/data.yaml', args.gm))

        for faction in sorted(factions, key=lambda x: f'{tier_to_num[factions[x]["tier"]]}-{factions[x]["hold"]}-{x}'):
            print_faction_entry(factions[faction], args.gm, faction)

        factions_total = factions_total | factions
        print("</ul>")

    if not args.gm:
        create_image('map', factions_total)
        create_image('mitte', factions_total)
    print(f"<h1>Mapki</h1>")
    print(f'<p><a href="maps/berlin-mitte.jpg"><img src="maps/berlin-mitte.jpg" class="map"></a></p>')
    print(f'<p><a href="maps/berlin-map.jpg"><img src="maps/berlin-map.jpg" class="map"></a></p>')

    print('</div>')
    print("</body>")
    print("</html>")
