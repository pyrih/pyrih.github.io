from stravalib import Client
from stravalib.protocol import AccessInfo


class StravaAuthenticator:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str, client: Client):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.client = client

    def authenticate(self) -> None:
        access_info: AccessInfo = self.client.refresh_access_token(
            client_id=int(self.client_id),
            client_secret=self.client_secret,
            refresh_token=self.refresh_token
        )
        self.client.access_token = access_info['access_token']
        self.client.refresh_token = access_info['refresh_token']
