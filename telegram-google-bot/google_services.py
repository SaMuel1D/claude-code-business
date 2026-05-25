import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
]

TOKEN_FILE = "/tmp/token.json"
CREDENTIALS_FILE = "/tmp/credentials.json"


def _write_env_files():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if creds_json and not Path(CREDENTIALS_FILE).exists():
        Path(CREDENTIALS_FILE).write_text(creds_json)

    token_json = os.environ.get("GOOGLE_TOKEN_JSON")
    if token_json and not Path(TOKEN_FILE).exists():
        Path(TOKEN_FILE).write_text(token_json)


def get_credentials() -> Credentials:
    _write_env_files()

    creds = None
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            Path(TOKEN_FILE).write_text(creds.to_json())
        else:
            creds_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", CREDENTIALS_FILE)
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            Path(TOKEN_FILE).write_text(creds.to_json())

    return creds


def get_today_events() -> list:
    service = build("calendar", "v3", credentials=get_credentials())
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return result.get("items", [])


def get_week_events() -> list:
    service = build("calendar", "v3", credentials=get_credentials())
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return result.get("items", [])


def _fetch_mail_headers(service, msg_id: str) -> dict:
    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"],
    ).execute()
    headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
    return {
        "from": headers.get("From", "Unbekannt"),
        "subject": headers.get("Subject", "(kein Betreff)"),
    }


def get_unread_mails(max_results: int = 5) -> list:
    service = build("gmail", "v1", credentials=get_credentials())
    result = service.users().messages().list(
        userId="me", q="is:unread", maxResults=max_results
    ).execute()
    return [_fetch_mail_headers(service, m["id"]) for m in result.get("messages", [])]


def get_urgent_mails() -> list:
    service = build("gmail", "v1", credentials=get_credentials())
    query = (
        "is:unread (subject:URGENT OR subject:DRINGEND OR subject:WICHTIG "
        "OR subject:important OR subject:dringend OR is:starred)"
    )
    result = service.users().messages().list(
        userId="me", q=query, maxResults=10
    ).execute()
    return [_fetch_mail_headers(service, m["id"]) for m in result.get("messages", [])]
