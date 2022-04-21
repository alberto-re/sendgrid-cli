import os

import click
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


@click.command()
@click.option(
    "-f",
    "--from-address",
    help="Specify sender address",
    required=True,
)
@click.option("-t", "--to-address", help="Specify recipient(s)", required=True)
@click.option("-s", "--subject", help="Specify subject", required=True)
@click.option("-b", "--body", help="Specify message body", required=True)
def sendmail(from_address, to_address, subject, body):
    message = Mail(
        from_email=from_address,
        to_emails=to_address,
        subject=subject,
        html_content=body,
    )

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)


if __name__ == "__main__":
    sendmail()
