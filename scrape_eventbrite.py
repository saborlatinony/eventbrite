import requests
from bs4 import BeautifulSoup
import json

# URL of the Eventbrite page
url = "https://www.eventbrite.com/o/sabor-latino-18086879057"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Example data extraction (customize based on actual page structure)
events = []
event_counter = 1

print("Response content length:", len(response.content))

for event in soup.find_all('div', class_='search-event-card-wrapper'):
    title_tag = event.find('div', class_='eds-event-card__formatted-name--is-clamped')
    link_tag = event.find('a', class_='eds-event-card-content__action-link')
    description_tag = event.find('div', class_='eds-event-card-content__sub-title')
    image_tag = event.find('img', class_='eds-event-card-content__image')

    # Check if all tags are found
    if title_tag and link_tag and description_tag and image_tag:
        title = title_tag.text.strip()
        link = link_tag['href']
        description = description_tag.text.strip()
        image_link = image_tag['src']

        # Print debug information
        print(f"Event {event_counter}:")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Description: {description}")
        print(f"Image Link: {image_link}")
        print()

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
    else:
        print(f"Event {event_counter} - Missing data")
        print()

# Save data to JSON file
with open('eventbrite_data.json', 'w') as f:
    json.dump({"events": events}, f, indent=4)

print("Data scraped and saved to eventbrite_data.json")
