from fastapi import FastAPI
from routes import appointments, states, ai

app = FastAPI(title="AI Appointment Booking API")

app.include_router(appointments.router, prefix="/api")
app.include_router(states.router, prefix="/api") 
app.include_router(ai.router, prefix="/api") 


@app.get("/")
def root():
    return {"message": "API is running"}