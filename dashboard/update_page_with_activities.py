import os

from stravalib import Client

from dashboard.strava_activity_fetcher import StravaActivityFetcher
from dashboard.strava_authenticator import StravaAuthenticator
from dashboard.strava_service import StravaService

if __name__ == "__main__":
    # Load Strava credentials from environment variables
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    client = Client()
    authenticator = StravaAuthenticator(client_id, client_secret, refresh_token, client)
    fetcher = StravaActivityFetcher(client)

    service = StravaService(authenticator, fetcher)
    service.run()
