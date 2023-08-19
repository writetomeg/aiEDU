import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

def scrape_district_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    district_links = []
    for td in soup.find_all('td', {'class': 'city-district-link'}):
        a = td.find('a', href=True)
        if a:
            full_url = urljoin(url, a['href'])
            district_links.append(full_url)

    return district_links

def scrape_school_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    school_name = soup.find('h1', {'class': 'school-name'}).text.strip()
    school_website_tag = soup.find('a', {'data-ga-click-label': 'Website'})
    
    # If a tag with the website is found, get the href, else set as None
    if school_website_tag:
        school_website = school_website_tag['href']
    else:
        school_website = None
    
    # Find the phone number
    stat_items = soup.find_all("div", class_="school-stats-item")
    phone_number = "N/A"
    for tag in stat_items:
        if tag.text.strip().startswith("("):
            phone_number = tag.text.strip()
            break

    return school_name, school_website, phone_number

district_url = 'https://www.greatschools.org/schools/districts/Ohio/OH/'
district_links = scrape_district_links(district_url)

with open('school_websites.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['School Name', 'Website', 'Phone Number'])

    for link in district_links:
        try:
            school_name, school_website, phone_number = scrape_school_info(link)
            writer.writerow([school_name, school_website, phone_number])
        except Exception as e:
            print(f"Error scraping {link}: {e}")
