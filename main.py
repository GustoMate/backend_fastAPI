from fastapi import FastAPI
import uvicorn
from GustomateApp.signup.router import router as signup_router  # Correctly import the router

app = FastAPI()

app.include_router(signup_router)  # Include the router with the correct prefix

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
