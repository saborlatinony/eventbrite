import requests
import json
from datetime import datetime, timezone, timedelta
import pytz  # Import pytz to handle timezone conversions
import locale

# Set your Eventbrite Private Token
API_TOKEN = '5SY7RWAKD46F4KIWPWTH'

# Use the correct organization ID for Sabor Latino
organization_id = '280240325960'

# Set the locale for Spanish formatting
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Ensure you have Spanish locale set up on your system

# Eventbrite API endpoint for Sabor Latino organization events
url = f'https://www.eventbriteapi.com/v3/organizations/{organization_id}/events/'

# Headers for authorization using the Private Token
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Set the New York time zone using pytz
ny_timezone = pytz.timezone('America/New_York')

# Function to fetch events with pagination
def fetch_all_events():
    all_events = []
    continuation = None
    
    while True:
        # If there's a continuation token, add it to the request parameters
        params = {}
        if continuation:
            params['continuation'] = continuation
        
        # Send GET request to the Eventbrite API
        response = requests.get(url, headers=headers, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            # Add the events from this page to the all_events list
            all_events.extend(data['events'])
            
            # Check if there is a continuation token for more pages
            if data['pagination']['has_more_items']:
                continuation = data['pagination']['continuation']
            else:
                break  # No more pages, break out of the loop
        else:
            print(f"Failed to retrieve events. Status code: {response.status_code}")
            print("Response content:", response.text)
            break
    
    return all_events

# Fetch all events
events = fetch_all_events()

# Get the current date in New York time zone
today = datetime.now(ny_timezone).date()

# Function to get the day of the week in Spanish
def get_day_of_week_in_spanish(date):
    days_of_week = {
        0: 'Lunes', 
        1: 'Martes', 
        2: 'Miércoles', 
        3: 'Jueves', 
        4: 'Viernes', 
        5: 'Sábado', 
        6: 'Domingo'
    }
    return days_of_week[date.weekday()]

# Transform the events data into the required format and filter out past events
transformed_events = []
for event in events:
    # Parse the event's start date from UTC and convert to New York time
    event_start_date_utc = datetime.strptime(event['start']['utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    event_start_date_ny = event_start_date_utc.astimezone(ny_timezone)  # Convert UTC to New York time

    # Check if the event time is exactly 11:59 PM
    if event_start_date_ny.hour == 23 and event_start_date_ny.minute == 59:
        # If it is, subtract 1 minute to prevent it from rolling into the next day
        event_start_date_ny = event_start_date_ny - timedelta(minutes=1)

    event_start_date_only = event_start_date_ny.date()  # Get only the date part

    # Get the day of the week in Spanish
    day_of_week = get_day_of_week_in_spanish(event_start_date_ny)

    # Format the date as "Jueves 10 de Octubre, 2024"
    event_date_str = event_start_date_ny.strftime(f'{day_of_week} %d de %B, %Y')
    
    # Check if the event is happening today or in the future
    if event_start_date_only == today:
        description = f"HOY! {event_date_str}"  # "HOY!" before the date
    elif event_start_date_only > today:
        description = f"Este {event_date_str}."

    # Only include events after today or on today
    if event_start_date_only >= today:
        # Build the transformed event
        transformed_event = {
            "title": event['name']['text'],  # Event name
            "$id": event['id'],  # Event unique ID (required by Klaviyo)
            "description": description,  # Display "HOY!" for today's events, else event date in Spanish
            "$link": event['url'],  # Event URL (required by Klaviyo)
            "$image_link": event['logo']['url'] if event['logo'] else None,  # Event image (if available, required by Klaviyo)
            "price": 0,  # You can adjust this based on your ticket data
            "categories": [category['name'] for category in event['category']] if event.get('category') else []  # Categories
        }
        transformed_events.append(transformed_event)

# Save the transformed data to a new JSON file
with open('sabor_latino_custom_catalog.json', 'w') as json_file:
    json.dump(transformed_events, json_file, indent=4)

print(f"Transformed data saved to 'sabor_latino_custom_catalog.json'. Total future events: {len(transformed_events)}")
