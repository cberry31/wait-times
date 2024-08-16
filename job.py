from datetime import datetime
import logging
import os
import time
import pytz
from QueueTimes import QueueTimes
from SES import SES

# Park ID   | Park Name
# -------------------
# 16        | Disneyland
# 17        | Disney California Adventure
# 5         | Epcot
# 6         | Magic Kingdom
# 7         | Hollywood Studios
# 8         | Animal Kingdom


class Job:
    def __init__(self):
        self.queueTimes = QueueTimes()
        self.parkIds = [16, 17]
        self.queueTimes.setDesiredWaitTimes()
        self.queueTimes.setDesiredRides()
        self.ses = SES()

    def main(self):
        # TODO: Think about adding a redis cache to store the downRides list
        # TODO: Add a table in the email showing all of the rides that we are tracking

        allRides = self.getAllRides()

        # Check if any rides are back up
        newlyUpRides = self.queueTimes.checkIfRideBackUp(allRides)

        # Place the rides that are down into the downRides list
        self.queueTimes.placeDownRides(allRides)
        shortWait = self.queueTimes.isShortWait(allRides)

        logging.debug(f"Short Wait Already Notified: {self.queueTimes.shortWaitAlreadyNotified}")

        if len(newlyUpRides) > 0 or len(shortWait) > 0:
            logging.info(f"Newly Up Rides: {newlyUpRides}")
            logging.info(f"Short Wait: {shortWait}")
            email = self.formatEmail(shortWait, newlyUpRides)
            self.ses.sendEmail("Ride Status Update", email)

    def getAllRides(self):
        allRides = []
        for park in self.parkIds:
            waitTimes = self.queueTimes.getWaitTimes(park)
            for land in waitTimes["lands"]:
                ridesByLand = land["rides"]
                allRides.extend(self.queueTimes.filterRides(ridesByLand))
        return allRides

    def formatEmail(self, shortWait, newlyUpRides):
        email = ""
        if len(newlyUpRides) > 0:
            email += "<h3>Newly Up Rides:</h3>"
            email += "<ul>"
            for ride in newlyUpRides:
                email += f"<li>{ride['name']} is back up with a current wait time of {ride['wait_time']} minutes!</li>"
            email += "</ul>"
        if len(shortWait) > 0:
            email += "<h3>Short Wait Times:</h3>"
            email += "<ul>"
            for ride in shortWait:
                email += f"<li>{ride['name']} has a short wait time of {ride['wait_time']} minutes!</li>"
            email += "</ul>"
        currentTime = datetime.now(pytz.timezone("America/Los_Angeles")).strftime("%m/%d/%Y %H:%M:%S")
        email += f"<br/><br/><hr/><footer>Time sent at {currentTime}</footer>"
        logging.debug(f"Email: {email}")
        return email


if __name__ == "__main__":
    logging.basicConfig(
        filename="log.txt",
        level=os.environ.get("LOGGING_LEVEL", "INFO"),
        format="%(levelname)s:%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    logging.info("Starting job")
    job = Job()
    timeToSleep = 60
    while True:
        try:
            job.main()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(timeToSleep)
