import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class SES:
    def __init__(self):
        self.client = boto3.client(
            "ses",
            region_name=os.environ.get("AWS_REGION", "us-west-2"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.emailFrom = os.environ.get("EMAIL_FROM")
        self.emailTo = os.environ.get("EMAIL_TO")

    def sendEmail(self, subject: str, body: str):
        response = self.client.send_email(
            Destination={
                "ToAddresses": [self.emailTo],
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": body,
                    },
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": subject,
                },
            },
            Source=self.emailFrom,
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(f"Failed to send email: {response}")
        return response
