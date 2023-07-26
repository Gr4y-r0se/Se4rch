import requests
from bs4 import BeautifulSoup
import sys


def get_links(url, to_find):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            links = [
                link.get("href") for link in soup.find_all("a") if link.get("href")
            ]
            if to_find in response.text:
                hit = True
            else:
                hit = False
            return links, hit
        else:
            return [], False
    except:
        return [], False


def main(uri, to_find):
    # Replace this URL with the one you want to crawl
    starting_url = uri

    # List to store the crawled links
    crawled_links = []

    # Queue of URLs to crawl (starting with the initial URL)
    urls_to_crawl = [starting_url]

    while urls_to_crawl:
        current_url = urls_to_crawl.pop(0)  # Get the next URL to crawl
        crawled_links.append(
            current_url
        )  # Add the current URL to the list of crawled links
        sys.stdout.write("\033[K")
        print(f"Scanning: {current_url}", end="\r")

        # Get the links from the current URL
        links, hit = get_links(current_url, to_find)
        if hit == True:
            print(f"Hit on: {current_url}")
        links = [uri + i for i in links]
        # Add new links to the queue if they are not already crawled and not in the queue
        for link in links:
            if link not in crawled_links and link not in urls_to_crawl:
                urls_to_crawl.append(link)


if __name__ == "__main__":
    if "-h" in sys.argv or len(sys.argv) != 3:
        print("Usage: python3 crawl.py https://example.com whatIWantToFind")
    else:
        uri = sys.argv[1]
        searchterm = sys.argv[2]
        main(uri, searchterm)
