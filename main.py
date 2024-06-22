from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import get_database, users_collection, pizzas_collection
from routers.user import auth_router
from routers.orders import router as orders_router
from routers.admin import router as admin_router 
from schemas import UserModel
from pymongo.errors import PyMongoError
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

origins = [
    "http://127.0.0.1:8000/",  
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(admin_router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_current_user(request: Request):
    user = request.session.get("user")
    if user is None:
        return None
    return UserModel(**user)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: UserModel = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/admin_dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user: UserModel = Depends(get_current_user)):
    if user is None or not user.is_staff:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/orders", response_class=HTMLResponse)
async def user_dashboard(request: Request, user: UserModel = Depends(get_current_user)):
    if user is None or user.is_staff:
        return RedirectResponse(url="/login")

    try:
        db = get_database()
        pizzas = await db.pizzas.find({}, {"_id": 0}).to_list(length=100)
        return templates.TemplateResponse("orders.html", {"request": request, "pizzas": pizzas, "user": user})
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pizzas")
async def get_pizzas():
    try:
        db = get_database()
        pizzas = await db.pizzas.find({}, {"_id": 0}).to_list(length=100)
        return pizzas
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))
