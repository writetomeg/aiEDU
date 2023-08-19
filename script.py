import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the webpage with the list of URLs
page_urls = [
    "https://www.greatschools.org/schools/districts/Ohio/OH/"
    # Add the rest of the states here
]

for page_url in page_urls:
    # Send a GET request to the page URL
    page_response = requests.get(page_url)

    # Check if the request was successful
    if page_response.status_code == 200:
        # Parse the HTML content of the page
        page_soup = BeautifulSoup(page_response.content, "html.parser")
        
        # Find all divs with class "city-district-link"
        district_divs = page_soup.find_all(class_="city-district-link")
        
        # Create an array to store the absolute links
        absolute_links = []
        
        # Get the domain of the page
        base_url = "https://example.com"  # Replace with the actual domain
        
        # Iterate through each district div and extract the link
        for div in district_divs:
            link = div.find("a")
            if link and link.get("href"):
                absolute_link = urljoin(base_url, link.get("href"))
                absolute_links.append(absolute_link)
        
        # Now, for each absolute link, fetch the "data-ga-click-label" links
        for url in absolute_links:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                links = soup.find_all("a", {"data-ga-click-label": "Website"})
                href_links = [urljoin(url, link.get("href")) for link in links]
                print("Links for", url)
                for href in href_links:
                    print(href)
                print("-" * 40)
            else:
                print("Failed to retrieve page. Status code:", response.status_code)
    else:
        print("Failed to retrieve the page with URLs. Status code:", page_response.status_code)
