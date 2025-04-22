from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from db.database import create_db_and_tables
from routes import author, entry, category
from fastapi.templating import Jinja2Templates
from middlewares.logging import log_requests
import uvicorn
import requests
import json
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Registrar middlewares
app.middleware("http")(log_requests)

# Crea la base de datos y las tablas al iniciar la aplicación
@asynccontextmanager
async def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Get all entries.
    entriesURL = "http://127.0.0.1:8000/api/entries/"
    entries = requests.get(entriesURL).json()

    # Choose random entries.
    random1 = random.randrange(0, len(entries))
    random2 = -1
    random3 = -1
    if len(entries) > 2:
        while random2 == -1 or random2 == random1:
            random2 = random.randrange(0, len(entries))
        while random3 == -1 or random3 == random1 or random3 == random2:
            random3 = random.randrange(0, len(entries))

    maxLength = 150
    for entry in entries:
        if len(entry["content"]) > maxLength:
            entry["content"] = entry["content"][:maxLength - 3] + "..."

    return templates.TemplateResponse("index.html", {"request": request, "entries": entries, "random1": random1, "random2": random2, "random3": random3})

# Definir las rutas de la API
app.include_router(author.router, prefix="/api/authors", tags=["Authors"])
app.include_router(entry.router, prefix="/api/entries", tags=["Entries"])
app.include_router(category.router, prefix="/api/categories", tags=["Categories"])

# Manejo de excepciones globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred.", "error": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
