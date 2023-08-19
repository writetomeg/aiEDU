import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URLs of the webpages with the list of URLs
page_urls = [
    "https://www.greatschools.org/schools/districts/Ohio/OH/",
    "https://www.greatschools.org/schools/districts/Minnesota/MN/",
    "https://www.greatschools.org/schools/districts/Washington_Dc/DC/",
    # Add all of the states here
]

# Get the domain of the page
base_url = "https://www.greatschools.org"  # Replace with the actual domain

# Make a states folder if it doesn't exist
import os
if not os.path.exists("states"):
    os.mkdir("states")

# Iterate over each page URL
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

        # Iterate through each district div and extract the link
        for div in district_divs:
            link = div.find("a")
            if link and link.get("href"):
                absolute_link = urljoin(base_url, link.get("href"))
                absolute_links.append(absolute_link)

        # Write the URLs to a file named after the state
        state = page_url.split('/')[-2]
        with open(f"states/{state}.csv", "w") as f:
            # Now, for each absolute link, fetch the "data-ga-click-label" links
            school_count = 0
            for url in absolute_links:  
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    links = soup.find_all("a", {"data-ga-click-label": "Website"})
                    for link in links:
                        href = urljoin(url, link.get("href"))
                        school_name_tag = soup.find("h1", class_="school-name")
                        school_name = school_name_tag.text.strip() if school_name_tag else "N/A"
                        stat_items = soup.find_all("div", class_="school-stats-item")
                        phone_number = "N/A"
                        for tag in stat_items:
                            if tag.text.strip().startswith("("):
                                phone_number = tag.text.strip()
                                break

                        f.write(f"{school_name}, {href}, {phone_number}\n")
                        school_count += 1
                else:
                    print("Failed to retrieve page. Status code:", response.status_code)

            print(f"Successfully retrieved {school_count} schools in {state}")
    else:
        print("Failed to retrieve the page with URLs. Status code:", page_response.status_code)
