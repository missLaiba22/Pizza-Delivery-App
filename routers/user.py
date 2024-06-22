from fastapi import APIRouter, status, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import users_collection
from schemas import SignUpModel, LoginModel
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

templates = Jinja2Templates(directory="templates")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@auth_router.get('/signup', response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        # Check if the email already exists in the database
        db_email = await users_collection.find_one({"email": email})
        if db_email:
            return templates.TemplateResponse("signup.html",
                                              {"request": request, "error": "User with the email already exists. Please login."})

        # Check if the username already exists in the database
        db_username = await users_collection.find_one({"username": username})
        if db_username:
            return templates.TemplateResponse("signup.html",
                                              {"request": request, "error": "User with the username already exists. Please login."})

        # If email and username are unique, proceed with user creation
        hashed_password = generate_password_hash(password)
        new_user = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "is_active": True,
            "is_staff": False
        }

        await users_collection.insert_one(new_user)
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Error during signup: {e}")
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Internal Server Error"})


@auth_router.get('/login', response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post('/login', response_class=HTMLResponse)
async def login_for_access_token(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        db_user = await users_collection.find_one({"username": username})
        if db_user and check_password_hash(db_user["password"], password):
            request.session["user"] = {
                "username": db_user["username"],
                "email": db_user["email"],
                "is_staff": db_user["is_staff"],
                "is_active": db_user["is_active"],
                "role": db_user.get("role", "user"),  # assuming default role is "user"
                "user_id": str(db_user["_id"])  # Include the user_id in the session data
            }
            if db_user["is_staff"]:
                return RedirectResponse(url="/admin_dashboard", status_code=status.HTTP_303_SEE_OTHER)
            else:
                return RedirectResponse(url="/orders", status_code=status.HTTP_303_SEE_OTHER)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid Username Or Password"})

    except Exception as e:
        logger.error(f"Error during login: {e}")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Internal Server Error"})
