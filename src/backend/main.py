#!/usr/bin/env python3

import os
import logging
import json
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from typing import Optional, Dict
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define ServiceMetadata model
class ServiceMetadata(BaseModel):
    name: str
    description: str
    icon: str
    company: str
    version: str
    webpage: str
    route: Optional[str] = None
    new_page: Optional[bool] = None
    extra_query: Optional[str] = None
    avoid_iframes: Optional[bool] = None
    api: str
    sanitized_name: Optional[str] = None
    works_in_relative_paths: Optional[bool] = None
    extras: Optional[Dict[str, str]] = None

# Create FastAPI app
app = FastAPI(
    title="Mock BlueOS Extension",
    description="A sample BlueOS extension",
    version="0.0.1"
)

# Mount static files from frontend directory
app.mount("/frontend", StaticFiles(directory="/app/frontend", html=True), name="frontend")

# API routes
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Mock BlueOS Extension</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f5f5f5;
                }
                .container {
                    text-align: center;
                    padding: 2rem;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    max-width: 600px;
                }
                h1 {
                    color: #0066cc;
                    margin-bottom: 1rem;
                }
                p {
                    color: #666;
                    margin-bottom: 1.5rem;
                }
                .version {
                    font-size: 0.9rem;
                    color: #999;
                }
                .links {
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                    margin-top: 1.5rem;
                }
                .links a {
                    padding: 0.5rem 1rem;
                    background-color: #0066cc;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    transition: background-color 0.3s;
                }
                .links a:hover {
                    background-color: #0055aa;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Mock BlueOS Extension</h1>
                <p>A sample BlueOS extension demonstrating basic functionality.</p>
                <div class="version">Version 0.0.1</div>
                <div class="links">
                    <a href="/frontend/">Web Interface</a>
                    <a href="/docs">API Documentation</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/status")
async def status():
    return {"status": "running"}

@app.get("/cockpit_extras.json")
async def cockpit_extras():
    """
    Endpoint to provide cockpit extras configuration.
    Returns a JSON with actions configuration for the cockpit.
    """
    return {
        "actions": [
            {
                "id": "radcam-white-balance",
                "name": "Radcam White Balance",
                "type": "http-request",
                "config": {
                    "name": "Radcam White Balance",
                    "method": "POST",
                    "url": "http://{{ vehicle-address }}/extensionv2/radcam/auto_white_balance",
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "urlParams": {
                        "cam_id": 123
                    },
                    "body": ""
                }
            }
        ]
    }

@app.get("/register_service")
async def register_service():
    """
    Endpoint for BlueOS service registration.
    Returns metadata about this extension according to the ServiceMetadata model.
    """
    return ServiceMetadata(
        name="Mock BlueOS Extension",
        description="A sample BlueOS extension demonstrating basic functionality",
        icon="mdi-tools",  # Material Design Icons format
        company="BlueOS Extension Community",
        version="0.0.1",
        webpage="https://github.com/rafaellehmkuhl/MockBlueOsExtension",
        route="/frontend/index.html",
        new_page=False,
        avoid_iframes=False,
        api="/api",
        works_in_relative_paths=True,
        extras={
            "cockpit": "/cockpit_extras.json"
        }
    )

# WebSocket for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Run the server
    logger.info(f"Starting server on port {port}")
    uvicorn.run(
        "backend.main:app",  # Updated import path for Docker container
        host="0.0.0.0",
        port=port,
        reload=False
    )