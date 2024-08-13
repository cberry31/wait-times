import logging
import requests
import yaml


class QueueTimes:
    def __init__(self):
        # Will want to have different rides with wait times for notifications
        self.downRides = []
        self.desiredWaitTimes = {}
        self.desiredRides = []
        self.shortWaitAlreadyNotified = []

    def setDesiredWaitTimes(self):
        with open("rides.yaml", "r") as file:
            waitTimes = yaml.safe_load(file)
            self.desiredWaitTimes = waitTimes["wait_times"]

    def setDesiredRides(self):
        with open("rides.yaml", "r") as file:
            rides = yaml.safe_load(file)
            self.desiredRides = rides["rides"]

    def filterRides(self, rides: list):
        if len(self.desiredRides) == 0:
            return rides
        return [ride for ride in rides if ride["id"] in self.desiredRides]

    def getDownRides(self):
        return self.downRides

    def getWaitTimes(self, parkId: int):
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        waitTimes = requests.get(f"https://queue-times.com/parks/{parkId}/queue_times.json", headers=headers)
        if waitTimes.status_code != 200:
            logging.error(f"Failed to get wait times for park {parkId}")
            raise Exception(f"Failed to get wait times for park {parkId}")
        return waitTimes.json()

    def checkIfRideBackUp(self, rides: list):
        newlyUpRides = []
        for ride in rides:
            if ride["is_open"] is True and ride["id"] in self.downRides:
                self.downRides.remove(ride["id"])
                newlyUpRides.append(ride)
                logging.debug(f"{ride['name']} is back up!")
        return newlyUpRides

    def placeDownRides(self, rides: list):
        for ride in rides:
            if ride["is_open"] is False and ride["id"] not in self.downRides:
                self.downRides.append(ride["id"])

    def isShortWait(self, rides: list):
        shortWait = []
        logging.debug(f"Short Wait Already Notified: {self.shortWaitAlreadyNotified}")
        for ride in rides:
            if ride["id"] in self.shortWaitAlreadyNotified and ride["wait_time"] > self.desiredWaitTimes[ride["id"]]:
                logging.debug(f"{ride['name']} has a long wait time of {ride['wait_time']} minutes!")
                self.shortWaitAlreadyNotified.remove(ride["id"])
            if (
                ride["id"] in self.desiredWaitTimes
                and ride["is_open"]
                and ride["id"] not in self.shortWaitAlreadyNotified
                and ride["wait_time"] <= self.desiredWaitTimes[ride["id"]]
            ):
                shortWait.append(ride)
                self.shortWaitAlreadyNotified.append(ride["id"])
                logging.debug(f"{ride['name']} has a short wait time of {ride['wait_time']} minutes!")
        return shortWait
