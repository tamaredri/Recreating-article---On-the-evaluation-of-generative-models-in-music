# xml files source - https://github.com/owencm/hooktheory-data

import os
import re
import xml.etree.ElementTree as ET

# Directory paths
input_dir = '../hooktheory-data/xml'  # Change this to your input folder path
output_dir = '../xml_new'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


def clean_filename(name):
    name = re.sub(r' \(.*?\)', '', name)
    name = re.sub(r'\\\'', '', name)
    name = name.lower().replace(' ', '-')
    return name


def process_xml_file(file_path):
    print(file_path.split('\\')[-1])

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove XML declaration and outer <super> tag
    lines = [line for line in lines if not line.strip().startswith('<?xml') and not line.strip().startswith(
        '<super') and not line.strip().startswith('</super')]

    # Join lines to create a single string
    content = ''.join(lines)

    # Extract artist and title
    artist_search = re.search(r'<artist>(.*?)</artist>', content)
    title_search = re.search(r'<title>(.*?)</title>', content)

    if artist_search and title_search:
        artist = artist_search.group(1)
        title = title_search.group(1)

        # Convert artist and title to the required format
        artist_folder = clean_filename(artist)
        title_filename = clean_filename(title) + '.xml'

        # Create the new directory if it doesn't exist
        artist_dir = os.path.join(output_dir, artist_folder)
        os.makedirs(artist_dir, exist_ok=True)

        # Create new XML structure
        new_content = f"<theorytab>\n  <version>1.3</version>\n{content}\n</theorytab>"

        # Save the new XML file
        new_file_path = os.path.join(artist_dir, title_filename)
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content)


def main():
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            file_path = os.path.join(input_dir, filename)
            process_xml_file(file_path)


if __name__ == '__main__':
    main()
