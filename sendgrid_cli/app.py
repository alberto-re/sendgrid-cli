import base64
import os
from mimetypes import guess_type
from pathlib import Path
from typing import List, Tuple
from uuid import uuid4

import click
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    ContentId,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)

ATTACHMENT_DEFAULT_CONTENT_DISPOSITION = "attachment"

load_dotenv()


def unpack_addresses(addresses: Tuple[str]) -> List[Tuple[str, str]]:
    to_emails = []
    for addr in addresses:
        parts = addr.split(" ")
        if len(parts) > 1:
            to_emails.append((parts[-1], " ".join(parts[:-1])))
        else:
            to_emails.append((addr, ""))
    return to_emails


@click.command()
@click.option(
    "-f",
    "--from-address",
    help="Specify sender address",
    required=True,
)
@click.option(
    "-t", "--to-address", help="Specify recipient(s)", required=True, multiple=True
)
@click.option(
    "-c", "--cc-address", help="Specify carbon copy recipient(s)", multiple=True
)
@click.option(
    "--bcc-address", help="Specify blind carbon copy recipient(s)", multiple=True
)
@click.option("-s", "--subject", help="Specify subject", required=True)
@click.option("-b", "--body", help="Specify message body", required=True)
@click.option("-a", "--attach", help="Specify an attachment")
def sendmail(from_address, to_address, cc_address, bcc_address, subject, body, attach):

    message = Mail(
        from_email=from_address,
        to_emails=unpack_addresses(to_address),
        subject=subject,
        html_content=body,
    )
    if cc_address:
        message.cc_emails = unpack_addresses(cc_address)
    if bcc_address:
        message.bcc_emails = unpack_addresses(bcc_address)

    if attach:
        attachment_path = Path(attach)
        if not attachment_path.is_file():
            raise IOError()

        with open(attachment_path, "rb") as f:
            data = f.read()

        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType(guess_type(attachment_path)[0])
        attachment.file_name = FileName(attachment_path.name)
        attachment.disposition = Disposition(ATTACHMENT_DEFAULT_CONTENT_DISPOSITION)
        attachment.content_id = ContentId(str(uuid4()))
        message.attachment = attachment

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)


if __name__ == "__main__":
    sendmail()
