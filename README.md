# Sandbox

Generate curated, pre-tagged datasets using the Outbound Dialler API

## Usage

Install dependencies
```commandline
poetry install
```

Run the server
```commandline
poetry run sandbox
```

The server will be listening on port 3000!

## Credentials

You will need to load the following as environment variables, before running the server.

For the slack app:
```commandline
SLACK_BOT_TOKEN
SLACK_SIGNING_SECRET
```

For the internal api:
```commandline
API_BASEPATH
OUTBOUND_DIALLER_EMAIL
OUTBOUND_DIALLER_PASSWORD
```