from app.router import wikis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

app = FastAPI(
    title="Wiki Service",
    description="Microservice for managing wikis",
    version="v1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(wikis)


@app.get("/")
def main_route():
    return RedirectResponse(url="/docs")
