import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

# Данные о сервисе
SERVICE_NAME = os.getenv("SERVICE_NAME", "Default Service")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0")
SERVICE_PORT = os.getenv("PORT", "8000")
RELATED_SERVICES = os.getenv("RELATED_SERVICES", "").split(",")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    related_info = ""
    if RELATED_SERVICES and RELATED_SERVICES[0]:
        async with httpx.AsyncClient() as client:
            for service_url in RELATED_SERVICES:
                service_url = service_url.strip()  # Удаление пробелов
                try:
                    response = await client.get(service_url)
                    related_info += f"<li>{response.text}</li>"
                except httpx.RequestError:
                    related_info += f"<li><h2>Error fetching {service_url}</h2></li>"
    else: related_info += f"<li><h2>There are no related services</h2></li>"

    return f"""
    <html>
        <head>
            <title>{SERVICE_NAME} Info</title>
        </head>
        <body>
            <h1>Service Name: {SERVICE_NAME}</h1>
            <h2>Version: {SERVICE_VERSION}</h2>
            <h2>Related Services:</h2>
            <ul>
                {related_info}
            </ul>
        </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
