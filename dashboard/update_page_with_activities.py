import json
import os
from datetime import datetime, timedelta

from stravalib import Client
from stravalib.model import SummaryActivity
from stravalib.protocol import AccessInfo

if __name__ == "__main__":
    print("Application started...")

    # Load Strava credentials from environment variables
    client_id: str = os.getenv("STRAVA_CLIENT_ID")
    client_secret: str = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token: str = os.getenv("STRAVA_REFRESH_TOKEN")

    print(f"Client id = {client_id}")

    # Authenticate and refresh access token
    client: Client = Client()

    access_info: AccessInfo = client.refresh_access_token(
        int(client_id),
        client_secret,
        refresh_token
    )

    access_token = access_info['access_token']

    client.access_token = access_token
    client.refresh_token = access_info['refresh_token']

    # Load the last check time from file
    last_check_file = './dashboard/misc/last_check.json'
    if os.path.exists(last_check_file):
        with open(last_check_file, 'r') as f:
            last_check = datetime.fromisoformat(json.load(f)['last_check'])
    else:
        last_check = datetime.now() - timedelta(days=30)  # Default to 30 days ago

    # Fetch activities since last check
    activities = client.get_activities(after=last_check)

    # Collect activity data
    activity_data = []
    for act  in activities:
        activity: SummaryActivity = act
        activity_data.append({
            'name': str(activity.name),
            'distance': str(activity.distance),
            'moving_time': str(activity.moving_time),
            'elapsed_time': str(activity.elapsed_time),
            'start_date': str(activity.start_date.isoformat()),
        })

    # Update the last check time
    with open(last_check_file, 'w') as f:
        json.dump({'last_check': datetime.now().isoformat()}, f)

    # Load current content of the page (HTML or Markdown)
    page_file = 'index.html'  # Or whatever file you're updating
    with open(page_file, 'r') as f:
        page_content = f.read()

    # Add the new activities to the page content
    new_activities_html = "<h2>Recent Activities</h2><ul>"
    for activity in activity_data:
        new_activities_html += f"<li>{activity['name']} - {activity['distance']} meters on {activity['start_date']}</li>"
    new_activities_html += "</ul>"

    # Insert the new activities into the page content
    updated_content = page_content.replace("<!--ACTIVITIES_PLACEHOLDER-->", new_activities_html)

    # Write the updated content back to the file
    with open(page_file, 'w') as f:
        f.write(updated_content)

