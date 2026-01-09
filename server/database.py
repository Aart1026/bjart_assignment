from typing import Dict, List, Optional
from datetime import datetime
import uuid
from .models import Instrument, InstrumentType, OrderRequest, OrderResponse, OrderStatus, Trade, PortfolioItem, OrderSide, OrderStyle

class MemoryDB:
    def __init__(self):
        self.instruments: Dict[str, Instrument] = {}
        self.orders: Dict[str, OrderResponse] = {}
        self.trades: List[Trade] = []
        # Portfolio: Symbol -> {quantity, total_cost_basis}
        self.portfolio: Dict[str, Dict] = {} 
        self._initialize_instruments()

    def _initialize_instruments(self):
        # Seed some data
        data = [
            Instrument(symbol="RELIANCE", name="Reliance Industries", instrumentType=InstrumentType.EQUITY, lastTradedPrice=2500.0),
            Instrument(symbol="TCS", name="Tata Consultancy Services", instrumentType=InstrumentType.EQUITY, lastTradedPrice=3400.0),
            Instrument(symbol="INFY", name="Infosys", instrumentType=InstrumentType.EQUITY, lastTradedPrice=1450.0),
            Instrument(symbol="HDFCBANK", name="HDFC Bank", instrumentType=InstrumentType.EQUITY, lastTradedPrice=1600.0),
            Instrument(symbol="NIFTY24JANFUT", name="Nifty Jan Future", instrumentType=InstrumentType.FUTURE, lastTradedPrice=21500.0),
        ]
        for inst in data:
            self.instruments[inst.symbol] = inst

    def get_instruments(self) -> List[Instrument]:
        return list(self.instruments.values())

    def get_instrument(self, symbol: str) -> Optional[Instrument]:
        return self.instruments.get(symbol)

    def create_order(self, order_request: OrderRequest) -> OrderResponse:
        order_id = str(uuid.uuid4())
        
        # Initial status is NEW
        order = OrderResponse(
            orderId=order_id,
            symbol=order_request.symbol,
            quantity=order_request.quantity,
            price=order_request.price,
            side=order_request.side,
            orderStyle=order_request.orderStyle,
            status=OrderStatus.NEW,
            timestamp=datetime.now()
        )
        
        self.orders[order_id] = order
        
        # Process Simulation immediately for simplicity
        self._process_order(order)
        
        return order

    def _process_order(self, order: OrderResponse):
        instrument = self.get_instrument(order.symbol)
        if not instrument:
            order.status = OrderStatus.REJECTED
            order.message = "Instrument not found"
            return

        execution_price = 0.0

        # Simulation Logic
        if order.orderStyle == OrderStyle.MARKET:
            execution_price = instrument.lastTradedPrice
            order.status = OrderStatus.EXECUTED
            order.price = execution_price # Update order price to execution price for record
        
        elif order.orderStyle == OrderStyle.LIMIT:
            # Simple simulation: 
            # BUY: Exec if Limit Price >= Market Price
            # SELL: Exec if Limit Price <= Market Price
            # Else: PLACED (Pending)
            if order.side == OrderSide.BUY:
                if order.price >= instrument.lastTradedPrice:
                    execution_price = order.price # In real world, could be lower, but let's say it executes at limit or LTP. Let's use LTP for realism if better.
                    # Usually: executes at best available. if LTP < Limit, use LTP. 
                    execution_price = min(order.price, instrument.lastTradedPrice)
                    order.status = OrderStatus.EXECUTED
                else:
                    order.status = OrderStatus.PLACED
            elif order.side == OrderSide.SELL:
                if order.price <= instrument.lastTradedPrice:
                    execution_price = max(order.price, instrument.lastTradedPrice)
                    order.status = OrderStatus.EXECUTED
                else:
                    order.status = OrderStatus.PLACED

        if order.status == OrderStatus.EXECUTED:
            self._create_trade(order, execution_price)

    def _create_trade(self, order: OrderResponse, price: float):
        trade = Trade(
            tradeId=str(uuid.uuid4()),
            orderId=order.orderId,
            symbol=order.symbol,
            quantity=order.quantity,
            price=price,
            side=order.side,
            timestamp=datetime.now()
        )
        self.trades.append(trade)
        self._update_portfolio(trade)

    def _update_portfolio(self, trade: Trade):
        # Simple Portfolio logic
        # Average Price implementation
        current_holding = self.portfolio.get(trade.symbol, {"quantity": 0, "total_cost": 0.0})
        
        if trade.side == OrderSide.BUY:
            current_holding["quantity"] += trade.quantity
            current_holding["total_cost"] += (trade.quantity * trade.price)
        elif trade.side == OrderSide.SELL:
            # For Sell, we reduce quantity. We don't change average buy price usually, but strict accounting varies.
            # Simplified: Reduce quantity. Realized PnL is not tracked here strictly, just holdings.
            # However, if we go negative (short), logic gets complex. Let's assume Long only or simple netting.
            current_holding["quantity"] -= trade.quantity
            if current_holding["quantity"] < 0:
                # Short support? Let's just allow negative quantity.
                pass
            
            # If we sell, we reduce total_cost proportional to quantity sold to keep avg price same?
            # Or we just keep track of avg buy price.
            # Let's simple model: Avg Price = Total Cost / Quantity.
            # When buying, update avg price. When selling, avg price stays same (FIFO/Weighted Avg), just reduce qty.
            pass  # Cost basis doesn't change on sell for the remaining shares.
            # But "total_cost" in this dict is used to calculate avg. 
            # So we should actually store avg_price and quantity.
            pass
        
        # Let's refine the dict structure to avoid confusion
        # We need to recalculate Average Price ONLY on BUY.
        # On SELL, Average Price doesn't change.
        
        entry = self.portfolio.get(trade.symbol)
        if not entry:
            entry = {"quantity": 0, "avg_price": 0.0}
        
        if trade.side == OrderSide.BUY:
            old_qty = entry["quantity"]
            old_cost = old_qty * entry["avg_price"]
            new_cost = old_cost + (trade.quantity * trade.price)
            new_qty = old_qty + trade.quantity
            entry["quantity"] = new_qty
            entry["avg_price"] = new_cost / new_qty if new_qty != 0 else 0.0
            
        elif trade.side == OrderSide.SELL:
            entry["quantity"] -= trade.quantity
        
        if entry["quantity"] == 0:
            entry["avg_price"] = 0.0
            
        self.portfolio[trade.symbol] = entry

    def get_order(self, order_id: str) -> Optional[OrderResponse]:
        return self.orders.get(order_id)

    def get_trades(self) -> List[Trade]:
        return self.trades

    def get_portfolio(self) -> List[PortfolioItem]:
        items = []
        for symbol, data in self.portfolio.items():
            if data["quantity"] == 0:
                continue
                
            inst = self.get_instrument(symbol)
            ltp = inst.lastTradedPrice if inst else 0.0
            
            val = data["quantity"] * ltp
            # PnL = (LTP - Avg) * Qty
            pnl = (ltp - data["avg_price"]) * data["quantity"]
            
            items.append(PortfolioItem(
                symbol=symbol,
                quantity=data["quantity"],
                averagePrice=data["avg_price"],
                currentValue=val,
                pnl=pnl
            ))
        return items

# Singleton instance
db = MemoryDB()
