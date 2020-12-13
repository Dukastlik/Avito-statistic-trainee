from fastapi import FastAPI
from routes import router
from db.mongodb_utils import connect_to_mongo, close_mongo_connection


app = FastAPI()
app.include_router(router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to AvitoStat app!"}


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
