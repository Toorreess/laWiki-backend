from fastapi import HTTPException

from app.database import MongoDBRepository
from app.models import WikiIn
from app.utils import replace_document_id

dbClient = MongoDBRepository(
    uri="mongodb+srv://torres:qlOJRgVu4owaLb74@cluster0.es98v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    database_name="laWiki",
    collection_name="Wiki",
)


def create_wiki(wiki: WikiIn):
    result = dbClient.insert_document(dict(wiki))
    return replace_document_id(dbClient.find_document(str(result.inserted_id)))


def get_wiki(wiki_id: str) -> dict:
    result = dbClient.find_document(wiki_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Wiki not found")

    return replace_document_id(result)


def update_wiki(wiki_id: str, updates: dict):
    if "id" in updates:
        updates.pop("id")

    if "deleted" in updates:
        updates.pop("deleted")

    dbClient.update_document(wiki_id, updates)

    return replace_document_id(dbClient.find_document(wiki_id))


def delete_wiki(wiki_id: str):
    dbClient.update_document(wiki_id, {"deleted": True})
    return None


def list_wikis(limit: int = 10, skip: int = 0, query: dict = {}):
    db_result = dbClient.list_documents(query, limit, skip)

    result = {}
    result["items"] = [replace_document_id(item) for item in db_result]
    result["total"] = len(db_result)
    result["limit"] = limit
    result["skip"] = skip
    result["next_skip"] = skip + limit if result["total"] == limit else None
    result["previous_skip"] = None if (skip - limit) < 0 else skip - limit

    return result
