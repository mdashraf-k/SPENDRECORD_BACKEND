from fastapi import FastAPI
from databases.database import engine, Base
import models

app = FastAPI()

@app.get("/health")
def health_check():
    return "Health Good!!!"


Base.metadata.create_all(bind=engine)

# app.include_router(file name)