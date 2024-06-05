import requests
from bs4 import BeautifulSoup
import json

# URL of the Eventbrite page
url = "https://www.eventbrite.com/o/sabor-latino-18086879057"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Data extraction
events = []
event_counter = 1

print("Response content length:", len(response.content))

for event in soup.find_all('div', class_='search-event-card-wrapper'):
    title_tag = event.find('div', class_='eds-event-card__formatted-name--is-clamped')
    link_tag = event.find('a', class_='eds-event-card-content__action-link')
    description_tag = event.find('div', class_='eds-event-card-content__sub-title')
    image_tag = event.find('img', class_='eds-event-card-content__image')
    date_tag = event.find('div', class_='eds-event-card-content__sub-title')  # Assuming date is here
    location_tag = event.find('div', class_='card-text--truncated__one')  # Assuming location is here

    if title_tag and link_tag and description_tag and image_tag and date_tag and location_tag:
        title = title_tag.text.strip()
        link = link_tag['href']
        description = description_tag.text.strip()
        image_link = image_tag['src']
        date = date_tag.text.strip()
        location = location_tag.text.strip()

        print(f"Event {event_counter}:")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Description: {description}")
        print(f"Image Link: {image_link}")
        print(f"Date: {date}")
        print(f"Location: {location}")
        print()

        unique_id = f"event_{event_counter}"
        event_counter += 1

        events.append({
            "$id": unique_id,
            "$title": title,
            "$link": link,
            "$image_link": image_link,
            "$description": description,
            "$date": date,
            "$location": location
        })
    else:
        print(f"Event {event_counter} - Missing data")
        print()

# Save data to JSON file
with open('eventbrite_data.json', 'w') as f:
    json.dump({"events": events}, f, indent=4)

print("Data scraped and saved to eventbrite_data.json")
