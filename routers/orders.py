from fastapi import APIRouter, HTTPException, Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from database import get_database
from pymongo.errors import PyMongoError
from schemas import OrderUpdate, OrderCreate, OrderStatusUpdate

router = APIRouter()

class Pizza(BaseModel):
    flavor: str
    image: str



@router.get("/api/pizzas", response_model=List[Pizza])
async def get_pizzas(request: Request, db=Depends(get_database)):

    # checking session for authentication
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        pizzas = await db.pizzas.find().to_list(length=100)
        return pizzas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/orders", response_model=dict)
async def create_order(order: OrderCreate, request: Request, db=Depends(get_database)):

    # Retrieving user information from session data to associate the order with the logged-in user
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    print("Received order:", order)  # Logging the received order data

    order_dict = order.dict()
    order_dict.update({
        "user_id": user.get("user_id"),  # Assuming user_id is stored in session data
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    try:
        result = await db.orders.insert_one(order_dict)
        order_dict["_id"] = str(result.inserted_id)
        return order_dict
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/orders/{order_id}", response_model=dict)
async def update_order(order_id: str, order: OrderUpdate, request: Request, db=Depends(get_database)):
    # checking session for authentication
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    order_dict = {k: v for k, v in order.dict().items() if v is not None}
    if not order_dict:
        raise HTTPException(status_code=400, detail="Nothing to update")
    order_dict["updated_at"] = datetime.utcnow()
    try:
        result = await db.orders.update_one(
            {"_id": ObjectId(order_id), "user_id": user.get("user_id")},  # Checking user_id along with order_id
            {"$set": order_dict}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        updated_order = await db.orders.find_one({"_id": ObjectId(order_id)})
        updated_order["_id"] = str(updated_order["_id"])
        return updated_order
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/orders/{order_id}", response_model=dict)
async def delete_order(order_id: str, request: Request, db=Depends(get_database)):

    # checking session for authentication
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    try:
        result = await db.orders.delete_one({"_id": ObjectId(order_id), "user_id": user.get("user_id")})  
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"detail": "Order deleted"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/orders/{user_id}", response_model=List[dict])
async def get_user_orders(user_id: str, request: Request, db=Depends(get_database)):
    
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    # Checking if the user has permission to view orders
    if user.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        orders = await db.orders.find({"user_id": user_id}).to_list(length=100)
        for order in orders:
            order["_id"] = str(order["_id"])
        return orders
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=str(e))

