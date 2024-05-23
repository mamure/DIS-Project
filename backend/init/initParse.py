import requests
import random
from bs4 import BeautifulSoup

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

def filter_file_links(links):
    file_links = []
    for link in links:
        if link.endswith('.pgn'):  # Change the file extension as per your requirement
            file_links.append(link)
    return file_links
    

def main():
    url = "https://www.pgnmentor.com/files.html"
    response = requests.get(url)
    if response.status_code == 200:
        links = extract_links(response.content)
        file_links = filter_file_links(links)
        random_file_links = random.sample(file_links, 50)
        print(random_file_links)
    else:
        print("Error collecting links")
        
if __name__ == "__main__":
    main()