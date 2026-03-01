from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases.database import engine, Base
from routers import auth, users, groups, group_members, spends

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://10.59.106.97:5173",   # your Vite dev
    "https://spendrecord.in",
    "https://www.spendrecord.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return "Go to /docs"


Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(group_members.router)
app.include_router(spends.router)

