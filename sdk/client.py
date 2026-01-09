import requests
from typing import List, Dict, Optional, Union
from enum import Enum

class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class TradingSDK:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def get_instruments(self) -> List[Dict]:
        """Fetch list of tradable instruments"""
        url = f"{self.base_url}/api/v1/instruments"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def place_order(self, symbol: str, quantity: int, side: str, order_style: str = "MARKET", price: Optional[float] = None) -> Dict:
        """
        Place a new order.
        side: "BUY" or "SELL"
        order_style: "MARKET" or "LIMIT"
        price: Required if order_style is LIMIT
        """
        url = f"{self.base_url}/api/v1/orders"
        
        payload = {
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
            "orderStyle": order_style,
            "price": price
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def get_order_status(self, order_id: str) -> Dict:
        """Fetch order status by Order ID"""
        url = f"{self.base_url}/api/v1/orders/{order_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_trades(self) -> List[Dict]:
        """Fetch executed trades"""
        url = f"{self.base_url}/api/v1/trades"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_portfolio(self) -> List[Dict]:
        """Fetch current portfolio holdings"""
        url = f"{self.base_url}/api/v1/portfolio"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
