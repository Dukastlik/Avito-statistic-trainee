from fastapi import FastAPI
from routes import router
from db.mongodb_utils import connect_to_mongo, close_mongo_connection
from api.update import update_on_startup

app = FastAPI()

app.include_router(router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to AvitoStats app!"}

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("startup", update_on_startup)
app.add_event_handler("shutdown", close_mongo_connection)




