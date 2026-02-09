from fastapi import FastAPI
from databases.database import engine, Base
from routers import auth, users

app = FastAPI()

@app.get("/")
def health_check():
    return "Go to /docs"


Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)