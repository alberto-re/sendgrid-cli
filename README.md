# sendgrid-cli

A command line tool to send emails through SendGrid APIs.

## Requirements

- Python 3.10
- [Poetry](https://python-poetry.org/) (tested with v1.1.3, current stable version)

## Installation

### Install dependencies with Poetry

Place yourself in the root of the project and execute in a terminal the command:

```
poetry install
```

### Export SENDGRID_API_KEY environment variable

You can either export the variable directly on your terminal session before
running the application, like this:

```
export SENDGRID_API_KEY=<YOUR_API_KEY_VALUE>
```

or copy the provided _.env.dist_ file as a new file named _.env_ in the same
directory and insert into the newly created file your SendGrid API key.

## Usage

### Show usage and options

```
$ poetry run sendmail -h
Usage: sendmail [OPTIONS]

Options:
  -f, --from-address TEXT   Specify sender address  [required]
  -t, --to-address TEXT     Specify recipient(s)  [required]
  -c, --cc-address TEXT     Specify carbon copy recipient(s)
  --bcc-address TEXT        Specify blind carbon copy recipient(s)
  -s, --subject TEXT        Specify subject  [required]
  -b, --body TEXT           Specify message body
  -a, --attach TEXT         Specify an attachment
  -i, --template-id TEXT    Specify a template ID
  -d, --template-data TEXT  Specify template data
  -h, --help                Show this message and exit.
```

### Send an email

```
poetry run sendmail \
  -f me@example.com \
  -t you@example.com \
  -s "SendGrid is awesome" \
  -b "SendGrid is <b>awesome</b>"
Email sent successfully
```

### Send an email loading HTML body from a file

```
poetry run sendmail \
  -f me@example.com \
  -t you@example.com \
  -s "SendGrid is awesome" \
  -b file:/tmp/template.html
Email sent successfully
```

### Send an email to multiple recipients

Just specify multiple times the _-t, --to-address_ option:

```
poetry run sendmail \
  -f me@example.com \
  -t you@example.com \
  -t him@example.com \
  -s "SendGrid is awesome" \
  -b file:/tmp/template.html
Email sent successfully
```

### Specify CC/BCC additional recipients

Use respectively _-c, --cc-address_ or _-bcc-address_. Both options work just like
the _-t, --to-address_ option:

```
poetry run sendmail \
  -f me@example.com \
  -t you@example.com \
  --bcc-address him@example.com \
  -s "SendGrid is awesome" \
  -b file:/tmp/template.html
Email sent successfully
