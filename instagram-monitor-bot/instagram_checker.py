import instaloader
import logging
from datetime import datetime, timezone
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

logger = logging.getLogger(__name__)

_loader = None


def get_loader() -> instaloader.Instaloader:
    global _loader
    if _loader is None:
        _loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True,
        )
        if INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD:
            try:
                _loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
                logger.info("Instagram-Login erfolgreich")
            except Exception as e:
                logger.warning(f"Instagram-Login fehlgeschlagen: {e}")
    return _loader


def fetch_new_posts(account: str, last_shortcode: str | None, max_posts: int = 10) -> list[dict]:
    """Gibt neue Posts zurück, die nach last_shortcode erschienen sind."""
    loader = get_loader()
    new_posts = []

    try:
        profile = instaloader.Profile.from_username(loader.context, account)
        posts_iter = profile.get_posts()

        for post in posts_iter:
            if post.shortcode == last_shortcode:
                break
            post_data = {
                "shortcode": post.shortcode,
                "url": f"https://www.instagram.com/p/{post.shortcode}/",
                "timestamp": post.date_utc,
                "is_video": post.is_video,
                "caption": (post.caption or "")[:200],
                "likes": post.likes,
                "account": account,
                "typename": post.typename,
            }
            new_posts.append(post_data)
            if len(new_posts) >= max_posts:
                break

    except instaloader.exceptions.ProfileNotExistsException:
        logger.error(f"Account nicht gefunden: {account}")
    except instaloader.exceptions.LoginRequiredException:
        logger.warning(f"Login erforderlich für: {account}")
    except Exception as e:
        logger.error(f"Fehler bei {account}: {e}")

    return list(reversed(new_posts))  # älteste zuerst
