
"""Notification microservice - entry point."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client.eureka_client import EurekaClient

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialisation du client Eureka
    client = EurekaClient(
        eureka_server="http://localhost:8761/eureka",
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="localhost",
        instance_ip="127.0.0.1",

        # URLs de santé et d'information
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info"
    )

    # Enregistrement dans Eureka
    await client.start()
    print("NOTIFICATION enregistré dans Eureka !")

    yield

    # Arrêt et désenregistrement
    await client.stop()
    print("NOTIFICATION arrêté et désenregistré de Eureka.")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description="Notification microservice",
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Health endpoint
@app.get("/health")
async def health():
    return {"status": "UP"}


# Info endpoint
@app.get("/info")
async def info():
    return {
        "name": "NOTIFICATION",
        "version": "1.0.0"
    }


# API routes existantes
app.include_router(notification.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)
