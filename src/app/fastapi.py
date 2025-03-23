from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware

import app
import app.domain
from app.api import endpoints, exception_handlers
from app.api.deps import user_token_dep_factory
from app.config import Settings
from app.containers import Container


def create_fastapi_app(project_name: str, version: str, description: str) -> FastAPI:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()

    config: Settings = Settings(**container.config())

    reusable_oauth2 = OAuth2PasswordBearer(
        tokenUrl=config.api.auth_uri,
        auto_error=False,
    )

    fastapi_app = FastAPI(
        title=project_name,
        version=version,
        description=description,
        docs_url=(config.api.prefix + "/docs") if config.api.show_docs else None,
        openapi_url=(config.api.prefix + "/openapi.json")
        if config.api.show_docs
        else None,
        container=container,
        dependencies=[Depends(user_token_dep_factory(reusable_oauth2))],
        default_response_class=ORJSONResponse,
    )

    # Integrate with Sentry
    if config.sentry.dsn:
        fastapi_app.add_middleware(SentryAsgiMiddleware)

    # Set all CORS enabled origins
    if config.api.cors_origins:
        fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.api.cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Setup endpoints
    fastapi_app.include_router(endpoints.router, prefix=config.api.prefix)

    # Setup exception handlers
    for exc, handler in exception_handlers.registry:
        fastapi_app.add_exception_handler(exc, handler)

    return fastapi_app


fastapi_app = create_fastapi_app(
    app.__project_name__, app.__version__, app.__api_description__
)
