import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Profile, Project, Contactmessage

app = FastAPI(title="Halimur Rasyid MP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Halimur Rasyid MP backend is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# Profile Endpoints
@app.get("/api/profile", response_model=List[Profile])
def get_profile():
    docs = get_documents("profile", {}, limit=1)
    # Convert ObjectId to str for Pydantic
    for d in docs:
        if "_id" in d and isinstance(d["_id"], ObjectId):
            d["_id"] = str(d["_id"])  # ignored by model
    return docs


@app.post("/api/profile")
def create_or_update_profile(profile: Profile):
    # Upsert: if a profile exists, replace; else create
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    existing = db["profile"].find_one({})
    data = profile.model_dump()
    if existing:
        db["profile"].update_one({"_id": existing["_id"]}, {"$set": {**data, "updated_at": db.command("serverStatus")["localTime"]}})
        return {"status": "updated"}
    else:
        _id = create_document("profile", data)
        return {"status": "created", "id": _id}


# Projects Endpoints
@app.get("/api/projects", response_model=List[Project])
def list_projects():
    docs = get_documents("project", {})
    for d in docs:
        if "_id" in d and isinstance(d["_id"], ObjectId):
            d["_id"] = str(d["_id"])  # ignored by model
    return docs


@app.post("/api/projects")
def add_project(project: Project):
    _id = create_document("project", project)
    return {"id": _id}


# Contact Endpoint
@app.post("/api/contact")
def contact(message: Contactmessage):
    _id = create_document("contactmessage", message)
    return {"id": _id, "status": "received"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
