from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from database import get_database
from bson import ObjectId

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin_dashboard")
async def admin_dashboard(request: Request, db=Depends(get_database)):

    # checking session for authentication
    user = request.session.get("user")
    if not user or not user.get("is_staff"):
        # Redirecting to login page or handle unauthorized access
        raise HTTPException(status_code=401, detail="Unauthorized access")

    orders = await db.orders.find().to_list(length=100)
    for order in orders:
        order["_id"] = str(order["_id"])
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "orders": orders})

@router.post("/admin/cancel_orders")
async def cancel_orders(request: Request, user_id: str = Form(...), db=Depends(get_database)):

    # checking session for authentication
    user = request.session.get("user")
    if not user or not user.get("is_staff"):
        
        # Redirecting to login page or handle unauthorized access
        raise HTTPException(status_code=401, detail="Unauthorized access")

    try:
        result = await db.orders.delete_many({"user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="No orders found for this user")
        return RedirectResponse(url="/admin_dashboard", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

