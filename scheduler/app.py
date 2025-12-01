from fastapi import FastAPI
from .database import engine
from . import models
from .routes import users, appointments, businesses


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Scheduler API")


@app.get("/")
def read_root():
    return {"message": "Business scheduler API is alive"}


app.include_router(businesses.router)
app.include_router(users.router)
app.include_router(appointments.router)