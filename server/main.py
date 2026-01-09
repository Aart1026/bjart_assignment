from fastapi import FastAPI, HTTPException, status
from typing import List
from .models import Instrument, OrderRequest, OrderResponse, Trade, PortfolioItem
from .database import db

app = FastAPI(
    title="Trading API Platform",
    description="A simplified trading platform simulation",
    version="1.0.0"
)

# Instruments API
@app.get("/api/v1/instruments", response_model=List[Instrument])
def get_instruments():
    """Fetch list of tradable instruments"""
    return db.get_instruments()

# Order Management APIs
@app.post("/api/v1/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(order: OrderRequest):
    """Place a New Order"""
    # Basic validation is handled by Pydantic Model
    return db.create_order(order)

@app.get("/api/v1/orders/{order_id}", response_model=OrderResponse)
def get_order_status(order_id: str):
    """Fetch Order Status"""
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Trade APIs
@app.get("/api/v1/trades", response_model=List[Trade])
def get_trades():
    """Fetch list of executed trades"""
    return db.get_trades()

# Portfolio APIs
@app.get("/api/v1/portfolio", response_model=List[PortfolioItem])
def get_portfolio():
    """Fetch current portfolio holdings"""
    return db.get_portfolio()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Trading API is running"}
