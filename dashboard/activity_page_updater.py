import calendar
import logging
from datetime import datetime

from file_manager import FileManager


class ActivityPageUpdater:
    def __init__(self, page_file: str):
        self.page_file = page_file

    def update_page_with_activities(self, activities: list) -> None:
        logging.info(f"Updating {self.page_file} with {len(activities)} activities.")
        activities_by_date = self._group_activities_by_date(activities)
        calendar_html = self._generate_calendar_html(activities_by_date)

        page_content = FileManager.load_file(self.page_file, "<html><body><!--CALENDAR_PLACEHOLDER--></body></html>")
        updated_content = page_content.replace("<!--CALENDAR_PLACEHOLDER-->", calendar_html)

        if updated_content != page_content:
            logging.debug("The page content has changed, saving updates.")
            FileManager.save_file(self.page_file, updated_content)
        else:
            logging.info("No changes detected in the page content.")

    def _group_activities_by_date(self, activities: list) -> dict:
        logging.debug("Grouping activities by date...")
        activities_by_date = {}
        for activity in activities:
            date_str = activity['start_date'].split('T')[0]
            time_str = activity['start_date'].split('T')[1][:5]
            if date_str not in activities_by_date:
                activities_by_date[date_str] = []
            activities_by_date[date_str].append(f"{activity['name']} - {activity['distance']} meters at {time_str}")
        return activities_by_date

    def _generate_calendar_html(self, activities_by_date: dict) -> str:
        now = datetime.now()
        cal = calendar.Calendar(firstweekday=6)  # Sunday as the first day of the week
        days_in_month = cal.monthdayscalendar(now.year, now.month)

        logging.debug("Generating HTML calendar with activities...")
        table_html = '<h2>Activity Calendar</h2><table border="1">'
        table_html += '<thead><tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead><tbody>'

        for week in days_in_month:
            table_html += '<tr>'
            for day in week:
                if day == 0:
                    table_html += '<td></td>'
                else:
                    date_str = f"{now.year}-{now.month:02d}-{day:02d}"
                    activities_html = "<br>".join(activities_by_date.get(date_str, []))
                    table_html += f'<td>{day}<br>{activities_html}</td>'
            table_html += '</tr>'

        table_html += '</tbody></table>'
        return table_html
