from selenium import webdriver
from bs4 import BeautifulSoup
import os
import urllib.request

base_url = "https://elys-network.gitbook.io/docs/"
sitemap_url = base_url + "sitemap.xml"
output_dir = "./elys-docs/"

os.makedirs(output_dir, exist_ok=True)
print(f"Fetching URLs from {sitemap_url} to scrape to {output_dir}")

# Fetch the sitemap and parse it
req = urllib.request.Request(
    sitemap_url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'
    }
)
response = urllib.request.urlopen(req)
sitemap_xml = response.read()
soup = BeautifulSoup(sitemap_xml, "lxml-xml")
driver = webdriver.Chrome()

visited_links = set()


def save_html(url, content):
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.join(output_dir, parsed_url.path.lstrip("/"))
    if not filename.endswith(".html"):
        filename = f"{filename}.html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def scrape(current_url):
    if current_url in visited_links:
        return
    visited_links.add(current_url)

    driver.get(current_url)
    page_content = driver.page_source
    save_html(current_url, page_content)

try:
    # Extract all URLs from the sitemap and scrape them
    for loc in soup.find_all("loc"):
        scrape(loc.get_text())
finally:
    driver.quit()

print("Scraping complete!")

# def scrape(current_url):
#     if current_url in visited_links:
#         return
#     visited_links.add(current_url)
    
#     modified_url = current_url.replace("/main/", "/v0.47/")
    
#     driver.get(modified_url)
#     page_content = driver.page_source
#     save_html(modified_url, page_content)