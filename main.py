from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from GustomateApp.account.router import router as signup_router 
from GustomateApp.recipe.router import router as recipe_router  
from GustomateApp.friend.router import router as friend_router
from GustomateApp.ingredients.router import router as ingredient_router
from GustomateApp.preference.router import router as preference_router
from GustomateApp.market.router import router as market_router
from GustomateApp.ocr.router import router as ocr_router


app = FastAPI()


SESSION_SECRET_KEY = "c6e65e55f2f1dafceacb3bbbda274420f11e3b6c5379c4133f0161b00c2ca581" #정식 배포전 변경, 분리 예정

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)


app.include_router(signup_router)
app.include_router(recipe_router)
app.include_router(friend_router)
app.include_router(ingredient_router)
app.include_router(preference_router)
app.include_router(market_router)
app.include_router(ocr_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
