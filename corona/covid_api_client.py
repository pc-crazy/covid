from datetime import datetime
import json

import requests


class ApiClient(object):

    def __init__(self, country=None):
        self.api_endpoint = "https://corona-api.com/countries/"
        self.country = country

    def get_time_line(self):
        try:
            response = requests.get(self.api_endpoint + self.country)
            if response.status_code == 200:
                return json.loads(response.content)["data"]["timeline"]
        except Exception as e:
            print(str(e))
            return []

    def get_records(self, start_date, end_date):
        history = self.get_time_line()
        fmt = "%Y-%m-%d"
        for timeline in history:
            date = datetime.strptime(timeline["date"], fmt)
            if start_date <= date.date() <= end_date:
                yield timeline
