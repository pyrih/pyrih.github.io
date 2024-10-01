import logging
import os

from stravalib import Client

from strava_activity_fetcher import StravaActivityFetcher
from strava_authenticator import StravaAuthenticator
from strava_service import StravaService

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Load Strava credentials from environment variables
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    logging.info("Starting Strava API client setup...")
    client = Client()
    authenticator = StravaAuthenticator(client_id, client_secret, refresh_token, client)
    fetcher = StravaActivityFetcher(client)

    service = StravaService(authenticator, fetcher)
    service.run()
