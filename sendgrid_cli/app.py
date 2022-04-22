#!/usr/bin/env python3

import base64
import json
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
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

load_dotenv()

sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))


def unpack_addresses(addresses: Tuple[str]) -> List[Tuple[str, str]]:
    to_emails = []
    for addr in addresses:
        parts = addr.split(" ")
        if len(parts) > 1:
            to_emails.append((parts[-1], " ".join(parts[:-1])))
        else:
            to_emails.append((addr, ""))
    return to_emails


def attach_to_message(file: str, message: Mail) -> None:
    path = Path(file)
    if not path.is_file():
        raise IOError()

    with open(path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.file_content = FileContent(encoded)
    attachment.file_type = FileType(guess_type(path)[0])
    attachment.file_name = FileName(path.name)
    attachment.disposition = Disposition(ATTACHMENT_DEFAULT_CONTENT_DISPOSITION)
    attachment.content_id = ContentId(str(uuid4()))
    message.attachment = attachment


@click.command(context_settings=CONTEXT_SETTINGS)
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
@click.option("-b", "--body", help="Specify message body (HTML)")
@click.option("-a", "--attach", help="Specify an attachment", multiple=True)
@click.option("-i", "--template-id", help="Specify a template ID")
@click.option("-d", "--template-data", help="Specify template data")
def sendmail(
    from_address,
    to_address,
    cc_address,
    bcc_address,
    subject,
    body,
    attach,
    template_data,
    template_id,
):

    if body and body.startswith("file:"):
        with open(body[5:], "r") as r:
            body = r.read()

    message = Mail(
        from_email=from_address,
        to_emails=unpack_addresses(to_address),
        subject=subject,
        html_content=body,
    )
    if cc_address:
        message.cc = unpack_addresses(cc_address)
    if bcc_address:
        message.bcc = unpack_addresses(bcc_address)

    for file in attach:
        attach_to_message(file, message)

    if template_data:
        message.dynamic_template_data = json.loads(template_data)
    if template_id:
        message.template_id = template_id

    try:
        sg.send(message)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email not sent, exception follows '{e}'")


if __name__ == "__main__":
    sendmail()
