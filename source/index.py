from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mangum import Mangum
from routes.index import (
    user,
    auth,
    health_check,
)

from config.index import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()

# add Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(auth)
app.include_router(health_check)

handler = Mangum(app)
