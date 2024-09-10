from datetime import datetime

from stravalib import Client


class StravaActivityFetcher:
    def __init__(self, client: Client):
        self.client = client

    def fetch_activities(self, after_date: datetime):
        return self.client.get_activities(after=after_date)
