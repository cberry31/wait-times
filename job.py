import time
from QueueTimes import QueueTimes


class Job:
    def __init__(self):
        self.queueTimes = QueueTimes()
        self.parkIds = [16, 17, 8, 7, 6, 5]

    def main(self):
        # TODO: What happens when the park closes - all the rides are down, we need a way to check if the park is closed
        # What we could do is at 3am we clear out the downRides list - this won't work since after all the rides will just go back
        newlyUpRides = []
        self.queueTimes.setDesiredWaitTimes()
        # self.queueTimes.setDesiredRides()
        for park in self.parkIds:
            waitTimes = self.queueTimes.getWaitTimes(park)
            for land in waitTimes["lands"]:
                rides = land["rides"]
                rides = self.queueTimes.filterRides(rides)
                if len(rides) == 0:
                    continue
                # Check if any rides are back up
                upRides = self.queueTimes.checkIfRideBackUp(rides)
                newlyUpRides.extend(upRides)
                # Place the rides that are down into the downRides list
                self.queueTimes.placeDownRides(rides)
                shortWait = self.queueTimes.isShortWait(rides)
        # print(self.queueTimes.getDownRides())
        if len(newlyUpRides) > 0 or len(shortWait) > 0:
            # TODO: Send a notification that the ride is back up
            print(newlyUpRides)
            print(shortWait)


if __name__ == "__main__":
    job = Job()
    timeToSleep = 60
    while True:
        try:
            job.main()
            time.sleep(timeToSleep)
        except Exception as e:
            print(e)
            time.sleep(timeToSleep)
