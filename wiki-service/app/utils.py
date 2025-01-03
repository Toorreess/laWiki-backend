def replace_document_id(document: dict):
    document["id"] = str(document["_id"])
    del document["_id"]
    return document
