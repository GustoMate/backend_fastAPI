from fastapi import FastAPI
import uvicorn
from GustomateApp.signup.router import router as signup_router 
from GustomateApp.recipe.router import router as recipe_router  

app = FastAPI()

app.include_router(signup_router)
app.include_router(recipe_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
