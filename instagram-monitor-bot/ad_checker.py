"""
Prüft die öffentliche Meta Ad Library auf aktive Anzeigen der Instagram-Accounts.
Keine Authentifizierung nötig — nutzt den öffentlichen Such-Endpoint.
"""
import requests
import logging
import time

logger = logging.getLogger(__name__)

AD_LIBRARY_URL = "https://www.facebook.com/ads/library/async/search_ads/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "de-DE,de;q=0.9",
    "Referer": "https://www.facebook.com/ads/library/",
}

# Mapping Instagram-Handle → Facebook-Page-Name für die Suche
# Kann manuell ergänzt werden, wenn bekannt
ACCOUNT_FB_NAMES = {
    "der_babyladen_erlangen": "Der Babyladen Erlangen",
    "mellermaerchenzwerge": "Märchenzwerge Melle",
    "maibee_neuenhagen": "Maibee Neuenhagen",
    "schuetzling_kindersitzladen": "Schützling Kindersitzladen",
    "baby_oelrichs": "Baby Oelrichs",
    "babyone_official": "BabyOne",
}


def search_ads(account: str, country: str = "DE") -> list[dict]:
    """Sucht in der Meta Ad Library nach aktiven Ads des Accounts."""
    search_name = ACCOUNT_FB_NAMES.get(account, account.replace("_", " "))
    params = {
        "q": search_name,
        "count": 10,
        "active_status": "active",
        "ad_type": "all",
        "countries[0]": country,
        "search_type": "keyword_unordered",
        "media_type": "all",
    }

    try:
        resp = requests.get(AD_LIBRARY_URL, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        # Die Antwort beginnt mit einem Security-Prefix, den wir entfernen
        text = resp.text
        for prefix in ("for (;;);", ")]}'\n"):
            if text.startswith(prefix):
                text = text[len(prefix):]
                break

        import json
        data = json.loads(text)
        ads_raw = data.get("payload", {}).get("results", [])

        ads = []
        for ad in ads_raw[:5]:
            ad_id = ad.get("adid", "")
            page_name = ad.get("page_name", "")
            ad_url = f"https://www.facebook.com/ads/library/?id={ad_id}" if ad_id else ""
            body_texts = [
                c.get("body", {}).get("text", "")
                for c in ad.get("snapshot", {}).get("cards", [])
                if c.get("body")
            ]
            caption = " | ".join(body_texts) or ad.get("snapshot", {}).get("caption", "")

            if page_name:
                ads.append({
                    "ad_id": ad_id,
                    "page_name": page_name,
                    "url": ad_url,
                    "caption": caption[:200],
                    "account": account,
                })

    except Exception as e:
        logger.warning(f"Ad Library-Abruf für {account} fehlgeschlagen: {e}")
        return []

    return ads


def check_all_accounts(accounts: list[str]) -> dict[str, list[dict]]:
    results = {}
    for account in accounts:
        results[account] = search_ads(account)
        time.sleep(2)  # Rate-Limiting vermeiden
    return results
