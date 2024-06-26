import requests
from bs4 import BeautifulSoup
import os


# Function to download ABC file from the tune page
def download_abc_file(tune_page_url, output_folder, name):
    if name == str(3):
        x = 2
    res = requests.get(tune_page_url)
    if(res.status_code != 200):
        res = requests.get(tune_page_url)

    s = BeautifulSoup(res.text, 'html.parser')
    tune_name = name + ".abc"  # You may need to adjust how the tune name is extracted

    # Find the first link with the text "abc"
    abc_link = s.find('a', text="abc")
    if abc_link:
        abc_url = abc_link['href']
        if not abc_url.startswith('http'):
            abc_url = "https://abcnotation.com" + abc_url
        abc_response = requests.get(abc_url)
        with open(os.path.join(output_folder, tune_name), 'w') as f:
            f.write(abc_response.text)
        print(f"Downloaded {tune_name} as {tune_name}")
    else:
        abc_pre = s.find('pre')
        if abc_pre:
            abc_text = abc_pre.text
            with open(os.path.join(output_folder, tune_name), 'w') as f:
                f.write(abc_text)
            print(f"No ABC link found, saved <pre> text as {tune_name}")
        else:
            print(f"No ABC link or <pre> tag found on page: {tune_page_url}")


# URL of the page containing the 66 jazz tunes
# 1. "https://abcnotation.com/searchTunes?q=jazz&f=c&o=a&s=0"
# 2. "https://abcnotation.com/searchTunes?q=jazz&f=c&o=a&s=10"
# 3. "https://abcnotation.com/searchTunes?q=jazz&f=c&o=a&s=20"
# 4. "https://abcnotation.com/searchTunes?q=jazz&f=c&o=a&s=30"

url = "https://abcnotation.com/searchTunes?q=jazz&f=c&o=a&s=50"

# Create output directory if it doesn't exist
abc_jazz_folder = "abc_jazz"
os.makedirs(abc_jazz_folder, exist_ok=True)

# Get the main page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <a> tags that contain "tune page"
tune_page_links = soup.find_all('a', text="tune page")

# Download ABC file from each tune page
for i, link in enumerate(tune_page_links):
    page_url = link['href']
    if not page_url.startswith('http'):
        page_url = "https://abcnotation.com" + page_url
    download_abc_file(page_url, abc_jazz_folder, 'page6_' + str(i))
