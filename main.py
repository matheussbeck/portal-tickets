from fastapi import FastAPI
from infra.configs.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)