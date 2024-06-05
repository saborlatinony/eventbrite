import requests
from bs4 import BeautifulSoup
import json

# URL of the Eventbrite page
url = "https://www.eventbrite.com/o/sabor-latino-18086879057"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Example data extraction (needs to be customized based on actual page structure)
events = []
for event in soup.find_all('div', class_='search-event-card-wrapper'):
    title = event.find('div', class_='eds-event-card__formatted-name--is-clamped').text.strip()
    date = event.find('div', class_='eds-event-card-content__sub-title').text.strip()
    location = event.find('div', class_='card-text--truncated__one').text.strip()
    link = event.find('a', class_='eds-event-card-content__action-link')['href']

    events.append({
        "title": title,
        "date": date,
        "location": location,
        "description": "",  # Add description extraction logic if available
        "link": link
    })

# Save data to JSON file
with open('eventbrite_data.json', 'w') as f:
    json.dump({"events": events}, f, indent=4)

print("Data scraped and saved to eventbrite_data.json")
