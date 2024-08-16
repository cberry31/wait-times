# Wait Times

### Description
This script monitors ride wait times and operational status based on data from rides.yaml. It performs the following tasks every minute:

1. Check Wait Times: It verifies if the wait times for rides are shorter than the thresholds specified in rides.yaml. If any ride's wait time meets or falls below the specified threshold, the script sends an email notification to the address provided in the .env file.

2. Monitor Ride Status: It tracks whether any rides that were previously down are now back up. For rides listed in the rides section of rides.yaml, if a ride recovers from being down, the script sends an email to notify the address in the .env file.

The script runs every minute to ensure timely updates on ride wait times and status changes.

### Prerequisites
- Python 3.11+
    - I am sure it will work with lower versions but I have not tested it
- AWS Account
- AWS SES set up with at least one verified email address

### Setup
1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add the following
    ```
    AWS_REGION=<Your AWS Region, THIS DEFAULTS TO us-west-2>
    AWS_ACCESS_KEY_ID=<Your AWS Access Key ID>
    AWS_SECRET_ACCESS_KEY=<Your AWS Secret Access Key>
    EMAIL_FROM=<Your AWS Email From>
    EMAIL_TO=<Your AWS Email To>
    LOGGING_LEVEL=<DEBUG, INFO, WARNING, ERROR, CRITICAL> # Default is INFO
    ```
4. Run `python job.py`
    - All logs will be written to `log.txt`
5. To view logs live run `tail -f log.txt`

### Modifying rides.yaml
- Update wait_times to the desired wait time in minutes in this format
    ```
    wait_times:
      ride_id: time_you_want_to_wait_in_minutes
    ```
- Update the rides section to include the rides you want to know when they are back up
    ```
    rides:
      - ride_id
    ```
- You can find the ride_id in `docs/allRides.yaml` or by going to the ride's page on [Queue-Times.com](https://queue-times.com/en-US) and looking at the URL
    - Example: `https://queue-times.com/en-US/parks/1/rides/1` the ride_id would be `1`

[Powered by Queue-Times.com](https://queue-times.com/en-US)