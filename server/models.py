from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime
import uuid

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    FUTURE = "FUTURE"
    OPTION = "OPTION"

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderStatus(str, Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class Instrument(BaseModel):
    symbol: str
    exchange: str = "NSE"
    instrumentType: InstrumentType
    lastTradedPrice: float
    name: str

class OrderRequest(BaseModel):
    symbol: str
    quantity: int
    price: Optional[float] = None  # Mandatory for LIMIT
    side: OrderSide
    orderStyle: OrderStyle
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

    @validator('price')
    def price_validation(cls, v, values):
        style = values.get('orderStyle')
        if style == OrderStyle.LIMIT and (v is None or v <= 0):
             raise ValueError('Price must be greater than 0 for LIMIT orders')
        return v

class OrderResponse(BaseModel):
    orderId: str
    symbol: str
    quantity: int
    price: Optional[float]
    side: OrderSide
    orderStyle: OrderStyle
    status: OrderStatus
    timestamp: datetime
    message: Optional[str] = None

class Trade(BaseModel):
    tradeId: str
    orderId: str
    symbol: str
    quantity: int
    price: float
    side: OrderSide
    timestamp: datetime

class PortfolioItem(BaseModel):
    symbol: str
    quantity: int
    averagePrice: float
    currentValue: float
    pnl: float = 0.0
