import hmac
import hashlib
import secrets

from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import db_helper, settings
from app.core.database import APIKey


def connector(func):
    """Decorator to connect to the database."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        async for session in db_helper.session_getter():
            try:
                result = await func(*args, session=session, **kwargs)
            finally:
                await session.close()
            return result

    return wrapper


async def generate_api_key() -> dict[str, str]:
    raw_key = secrets.token_urlsafe(32)
    digest = hmac.new(settings.secret.key.encode(), raw_key.encode(), hashlib.sha256).hexdigest()
    return {
        "api_key": raw_key,
        "digest": digest
    }


@connector
async def create_api_key(username: str, *, session: AsyncSession) -> dict[str, str]:
    keys = await generate_api_key()

    api_key = APIKey(
        username=username,
        key_hash=keys["digest"],
    )

    session.add(api_key)
    await session.commit()

    return {
        "api_key": keys["api_key"],
    }

if __name__ == "__main__":
    import asyncio

    username = input("Enter username: ")
    asyncio.run(create_api_key(username))