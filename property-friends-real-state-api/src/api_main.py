from ddtrace import patch
from fastapi import FastAPI
from v1_api import v1_api

patch(fastapi=True)
app = FastAPI(
    title="Property Friends Real State",
    description="API for predict property valuations",
    version=1
)

app.mount("/api/v1", v1_api)