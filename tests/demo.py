import sys
import os
import time

# Add project root to path so we can import sdk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sdk.client import TradingSDK, OrderType, OrderStyle

def run_demo():
    print("Initialize Trading SDK...")
    client = TradingSDK()

    # 1. Get Instruments
    print("\n--- Fetching Instruments ---")
    try:
        instruments = client.get_instruments()
        for idx, inst in enumerate(instruments):
            print(f"{idx+1}. {inst['symbol']} ({inst['name']}) - LTP: {inst['lastTradedPrice']}")
    except Exception as e:
        print(f"Failed to fetch instruments: {e}")
        return

    if not instruments:
        print("No instruments found.")
        return

    # 2. Place MARKET BUY Order
    symbol = "RELIANCE"
    qty = 10
    print(f"\n--- Placing MARKET BUY Order for {qty} {symbol} ---")
    try:
        order = client.place_order(symbol=symbol, quantity=qty, side=OrderType.BUY, order_style=OrderStyle.MARKET)
        print(f"Order Placed: ID={order['orderId']}, Status={order['status']}")
    except Exception as e:
        print(f"Failed to place order: {e}")
        return

    # 3. Check Order Status
    order_id = order['orderId']
    print(f"\n--- Checking Status for Order {order_id} ---")
    state = client.get_order_status(order_id)
    print(f"Current Status: {state['status']}")
    time.sleep(1) 

    # 4. Place LIMIT BUY Order (Below market price - should be PENDING)
    limit_price = 2000.0 
    print(f"\n--- Placing LIMIT BUY Order for {qty} {symbol} at {limit_price} (LTP is likely higher) ---")
    try:
        limit_order = client.place_order(symbol=symbol, quantity=qty, side=OrderType.BUY, order_style=OrderStyle.LIMIT, price=limit_price)
        print(f"Order Placed: ID={limit_order['orderId']}, Status={limit_order['status']}")
    except Exception as e:
        print(f"Failed to place limit order: {e}")

    # 5. Fetch Trades
    print("\n--- Fetching Executed Trades ---")
    trades = client.get_trades()
    for trade in trades:
        print(f"Trade ID: {trade['tradeId']}, Symbol: {trade['symbol']}, Qty: {trade['quantity']}, Price: {trade['price']}, Side: {trade['side']}")

    # 6. Fetch Portfolio
    print("\n--- Fetching Portfolio ---")
    portfolio = client.get_portfolio()
    for item in portfolio:
        print(f"Symbol: {item['symbol']}, Qty: {item['quantity']}, Avg Price: {item['averagePrice']:.2f}, Current Value: {item['currentValue']:.2f}, PnL: {item['pnl']:.2f}")

if __name__ == "__main__":
    run_demo()
