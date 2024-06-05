import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .. import init_app

APPLICATION_CONFIG = os.getenv('APPLICATION_CONFIG', 'local')


def init_sentry():
    """Initialize Sentry only if in production."""
    import sentry_sdk

    sentry_dsn = os.getenv('SENTRY_DSN')
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


def create_app():
    """Application factory function to create and configure a new FastAPI app instance.
    Args:
        config_name (Object): Object containing the application configuration

    Returns:
        Object: fastapi.FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        # Trailing slash causes CORS failures from these supported domains
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_app(app)

    if APPLICATION_CONFIG != 'local':
        init_sentry()
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

        app = SentryAsgiMiddleware(app)
    return app
