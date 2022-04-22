# sendgrid-cli

A command line tool to send emails through SendGrid APIs.

## Requirements

- Python 3.10
- [Poetry](https://python-poetry.org/) (tested with v1.1.3, current stable version)

## Installation

Place yourself in the root of the project and execute in a terminal the command:

```
poetry install
```

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
