import time
from QueueTimes import QueueTimes


def main():
    # TODO: What happens when the park closes - all the rides are down, we need a way to check if the park is closed
    # What we could do is at 3am we clear out the downRides list - this won't work since after all the rides will just go back
    queueTimes = QueueTimes()
    parkIds = [16, 17, 8, 7, 6, 5]
    while True:
        newlyUpRides = []
        queueTimes.setDesiredWaitTimes()
        # queueTimes.setDesiredRides()
        for park in parkIds:
            waitTimes = queueTimes.getWaitTimes(park)
            for land in waitTimes["lands"]:
                rides = land["rides"]
                rides = queueTimes.filterRides(rides)
                if len(rides) == 0:
                    continue
                # Check if any rides are back up
                upRides = queueTimes.checkIfRideBackUp(rides)
                newlyUpRides.extend(upRides)
                # Place the rides that are down into the downRides list
                queueTimes.placeDownRides(rides)
                shortWait = queueTimes.isShortWait(rides)
        # print(queueTimes.getDownRides())
        if len(newlyUpRides) > 0 or len(shortWait) > 0:
            # TODO: Send a notification that the ride is back up
            print(newlyUpRides)
            print(shortWait)
        # Sleep for 5 minutes
        time.sleep(300)


if __name__ == "__main__":
    main()
