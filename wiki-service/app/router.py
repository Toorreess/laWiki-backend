from fastapi import APIRouter

import app.endpoints as endpoints
import app.models as models

wikis = APIRouter(prefix="/wikis", tags=["wikis"])


@wikis.get("/")
def list_wikis(limit: int = 10, skip: int = 0, query: dict = {}):
    return endpoints.list_wikis(limit, skip, query)


@wikis.get("/{wiki_id}", response_model=models.WikiOut)
def get_wiki(wiki_id: str):
    return endpoints.get_wiki(wiki_id)


@wikis.post("/", response_model=models.WikiOut)
def create_wiki(wiki: models.WikiIn):
    return endpoints.create_wiki(wiki)


@wikis.patch("/{wiki_id}", response_model=models.WikiOut)
def update_wiki(wiki_id: str, updates: dict):
    return endpoints.update_wiki(wiki_id, updates)


@wikis.delete("/{wiki_id}", status_code=204)
def delete_wiki(wiki_id: str):
    return endpoints.delete_wiki(wiki_id)
