import logging
import time
from QueueTimes import QueueTimes

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

    def main(self):
        # TODO: Add in SES to send an email when a ride is back up
        # TODO: Think about adding a redis cache to store the downRides list
        # TODO: Add a table in the email showing all of the rides that we are tracking

        allRides = self.getAllRides()

        # Check if any rides are back up
        newlyUpRides = self.queueTimes.checkIfRideBackUp(allRides)

        # Place the rides that are down into the downRides list
        self.queueTimes.placeDownRides(allRides)

        shortWait = self.queueTimes.isShortWait(allRides)

        # logging.info(self.queueTimes.getDownRides())
        logging.debug(f"Short Wait: {shortWait}")
        logging.debug(f"Short Wait Already Notified: {self.queueTimes.shortWaitAlreadyNotified}")

        if len(newlyUpRides) > 0 or len(shortWait) > 0:
            # TODO: Send a notification that the ride is back up
            logging.info(f"Newly Up Rides: {newlyUpRides}")
            logging.info(f"Short Wait: {shortWait}")

    def getAllRides(self):
        allRides = []
        for park in self.parkIds:
            waitTimes = self.queueTimes.getWaitTimes(park)
            for land in waitTimes["lands"]:
                ridesByLand = land["rides"]
                allRides.extend(self.queueTimes.filterRides(ridesByLand))
        return allRides


if __name__ == "__main__":
    logging.basicConfig(
        filename="log.txt",
        level=logging.DEBUG,
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
