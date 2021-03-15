import csv
import glob
import json
import os
import fire
import requests
import yaml

from datetime import datetime
from bs4 import BeautifulSoup


class ReleaseTools:

    """Tools for collecting and managing release histories."""

    def _check_android_release(self, playstore_id):
        url = "https://play.google.com/store/apps/details"
        params = {"id": playstore_id, "hl": "en_US", "gl": "US"}
        r = requests.get(url, params)
        soup = BeautifulSoup(r.text, features="html.parser")

        div_version = soup.find("div", string="Current Version").parent
        version = div_version.contents[1].string

        div_updated = soup.find("div", string="Updated").parent
        release_date = datetime.strptime(div_updated.contents[1].string, "%B %d, %Y")

        div_new = soup.find("div", string="What's New").parent
        release_notes = div_new.contents[1].find("span").string

        row = [
            version.strip(),
            release_date.strftime("%Y-%m-%d"),
            release_notes.strip(),
        ]

        found = False
        with open("data/nhs-covid-19-releases-android.csv") as csvfile:
            reader = csv.reader(csvfile)
            for existing_row in reader:
                if existing_row == row:
                    found = True

        if not found:
            print("New version found")
            with open("data/nhs-covid-19-releases-android.csv", mode="a+") as csvfile:
                csvwriter = csv.writer(
                    csvfile,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                    lineterminator="\n",
                )
                csvwriter.writerow(row)
        else:
            print("No new version found")

    def _check_ios_release(self, appstore_id):
        """Get the lastest release from the Apple Appstore and update the CSV."""
        url = f"https://apps.apple.com/gb/app/{appstore_id}"
        request = requests.get(url)
        soup = BeautifulSoup(request.text, features="html.parser")
        div_new = soup.find("div", class_="whats-new__content")

        version = div_new.find("p", class_="whats-new__latest__version").string.replace(
            "Version", ""
        )
        release_date = datetime.strptime(
            div_new.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S.000Z"
        )
        release_notes = div_new.select("div.we-truncate p")[
            0
        ].text  # can contain tags e.g. <br/>, so use .text

        row = [
            version.strip(),
            release_date.strftime("%Y-%m-%d"),
            release_notes.strip(),
        ]

        found = False
        with open("data/nhs-covid-19-releases-ios.csv") as csvfile:
            reader = csv.reader(csvfile)
            for existing_row in reader:
                if existing_row == row:
                    found = True

        if not found:
            print("New version found")
            with open("data/nhs-covid-19-releases-ios.csv", mode="a+") as csvfile:
                csvwriter = csv.writer(
                    csvfile,
                    delimiter=",",
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL,
                    lineterminator="\n",
                )
                csvwriter.writerow(row)

        else:
            print("No new version found")

    def checkiosreleases(self):
        """
        Get the lastest releases for each ID sepcifed in
        scripts/config.yaml from the Google Play store
        and update the CSV.
        """
        config = yaml.safe_load(open("website/_config.yaml"))
        for id in config["appstore_ids"]:
            self._check_ios_release(id)

    def checkandroidreleases(self):
        """
        Get the lastest releases for each ID sepcifed in
        scripts/config.yaml from the Apple App Store and update the CSV.
        """

        config = yaml.safe_load(open("website/_config.yaml"))
        for id in config["playstore_ids"]:
            self._check_android_release(id)

    def checkreleases(self):
        """
        Get the lastest releases for each ID sepcifed in
        scripts/config.yaml from the Google Play store and Apple App
        Store and update the CSV.
        """

        self.checkiosreleases()
        self.checkandroidreleases()

    def updatetimestamp(self):

        """Update the timestamp base on the timestamp of the files contained in data/ ."""

        with open("datapackage.json", "r") as file:
            datapackage = json.load(file)

        updated = None
        for file_path in glob.glob("data/*.csv"):
            modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            if updated is None or modified > updated:
                updated = modified

        datapackage["updated"] = updated.isoformat()

        with open("datapackage.json", "w") as file:
            file.write(json.dumps(datapackage, indent=4))

        if updated is not None:
            print(f"Updated datapackage timestamp to {updated}")
        else:
            print("Datapackaged timestamp not updated")


if __name__ == "__main__":
    fire.Fire(ReleaseTools)
