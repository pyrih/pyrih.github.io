from datetime import datetime, timedelta

from activity_page_updater import ActivityPageUpdater
from file_manager import FileManager
from strava_activity_fetcher import StravaActivityFetcher
from strava_authenticator import StravaAuthenticator


class StravaService:
    LAST_CHECK_FILE = './dashboard/misc/last_check.json'
    PAGE_FILE = './index.html'

    def __init__(self, authenticator: StravaAuthenticator, fetcher: StravaActivityFetcher):
        self.authenticator = authenticator
        self.fetcher = fetcher

    def run(self) -> None:
        self.authenticator.authenticate()
        last_check = self._get_last_check_time()
        activities = self._fetch_new_activities(last_check)

        if activities:
            self._update_last_check_time()
            page_updater = ActivityPageUpdater(self.PAGE_FILE)
            page_updater.update_page_with_activities(activities)
        else:
            print("No new activities found. No updates made.")

    def _get_last_check_time(self) -> datetime:
        last_check_data = FileManager.load_json(self.LAST_CHECK_FILE)
        return datetime.fromisoformat(
            last_check_data.get('last_check', (datetime.now() - timedelta(days=30)).isoformat()))

    def _fetch_new_activities(self, last_check: datetime) -> list:
        raw_activities = self.fetcher.fetch_activities(after_date=last_check)
        return [
            {
                'name': str(activity.name),
                'distance': str(activity.distance),
                'moving_time': str(activity.moving_time),
                'elapsed_time': str(activity.elapsed_time),
                'start_date': str(activity.start_date.isoformat())
            }
            for activity in raw_activities
        ]

    def _update_last_check_time(self) -> None:
        FileManager.save_json(self.LAST_CHECK_FILE, {'last_check': datetime.now().isoformat()})
