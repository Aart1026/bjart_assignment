# Trading SDK & Simulated Backend

This project implements a bespoke Wrapper SDK and a simplified Trading API backend. It simulates core trading workflows such as viewing instruments, placing orders, and tracking portfolio holdings.

## Project Structure

```
.
├── server/
│   ├── main.py       # FastAPI Entry Point & Routes
│   ├── models.py     # Pydantic Domain Models
│   └── database.py   # In-Memory Database & Simulation Logic
├── sdk/
│   └── client.py     # Python SDK Wrapper
├── tests/
│   └── demo.py       # Verification Script
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

## Setup & Run Instructions

### Prerequisites
- Python 3.8+

### 1. Setup Environment
It is recommended to use a virtual environment.

```bash
# Create Virtual Environment
python3 -m venv venv

# Activate Virtual Environment
# Linux/Mac:
source venv/bin/activate
# Windows:
# .\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend Server

Start the FastAPI server. It will run on `http://127.0.0.1:8000`.

```bash
uvicorn server.main:app --reload
```
*The `--reload` flag is optional but useful for development.*

### 4. Run Verification Demo (SDK Usage)

In a new terminal (activate venv first), run the simulation script:

```bash
python tests/demo.py
```

## API Details (Backend)

Base URL: `http://127.0.0.1:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/instruments` | List available instruments |
| POST | `/api/v1/orders` | Place a new order |
| GET | `/api/v1/orders/{id}` | Get status of an order |
| GET | `/api/v1/trades` | List executed trades |
| GET | `/api/v1/portfolio` | Get current portfolio holdings |

### Swagger UI
Once the server is running, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the Interactive API Documentation (Swagger UI).

## SDK Usage Example

```python
from sdk.client import TradingSDK, OrderType, OrderStyle

client = TradingSDK()

# Get Instruments
instruments = client.get_instruments()
print(instruments)

# Place Order
order = client.place_order(
    symbol="RELIANCE", 
    quantity=10, 
    side=OrderType.BUY, 
    order_style=OrderStyle.MARKET
)
print(order)
```

## assumptions
- **Data Persistence**: Data is stored in-memory and will be lost when the server is restarted.
- **User Context**: The system assumes a single user environment. Authentication is bypassed/mocked.
- **Market Data**: Prices are static or simulated based on interaction (Limit orders check against static LTP).
