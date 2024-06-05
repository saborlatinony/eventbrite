import requests
from bs4 import BeautifulSoup
import json

# URL of the Eventbrite page
url = "https://www.eventbrite.com/o/sabor-latino-18086879057"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Example data extraction (needs to be customized based on actual page structure)
events = []
event_counter = 1
for event in soup.find_all('div', class_='search-event-card-wrapper'):
    title = event.find('div', class_='eds-event-card__formatted-name--is-clamped').text.strip()
    link = event.find('a', class_='eds-event-card-content__action-link')['href']
    description = event.find('div', class_='eds-event-card-content__sub-title').text.strip()
    image_link = event.find('img', class_='card-image__img')['src']

    # Generate a unique ID for each event
    unique_id = f"event_{event_counter}"
    event_counter += 1

    events.append({
        "$id": unique_id,
        "$title": title,
        "$link": link,
        "$image_link": image_link,
        "$description": description
    })

# Save data to JSON file
with open('eventbrite_data.json', 'w') as f:
    json.dump({"events": events}, f, indent=4)

print("Data scraped and saved to eventbrite_data.json")
