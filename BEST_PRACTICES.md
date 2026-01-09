# Best Practices Implementation Report

## Application Architecture

### 1. Layered Architecture (Separation of Concerns)
The application follows a clean layered architecture, ensuring separation of concerns:
- **Presentation Layer (API)**: `server/main.py` handles HTTP requests, status codes, and response formatting. It is decoupled from business logic.
- **Domain Layer (Models)**: `server/models.py` defines the core entities (Instrument, Order, Trade) using Pydantic. This ensures that the data structure is consistent across the application.
- **Data Access Layer (Repository)**: `server/database.py` manages data storage and retrieval. Although in-memory, it acts as a repository pattern implementation, allowing future replacement with a real DB without changing the API layer.

### 2. Singleton Pattern
The `MemoryDB` class acts as a Singleton (`db = MemoryDB()`), ensuring a single source of truth for the in-memory state across the application lifecycle.

## Application Development

### 1. Strong Typing & Validation
- **Pydantic Models**: Used extensively for request/response validation.
  - Automatic type checking (e.g., `quantity` must be int).
  - Custom validators (e.g., `quantity > 0`, `price` required for LIMIT orders).
- **Type Hints**: Python type hints (`List[Instrument]`, `Optional[float]`) are used throughout to improve code readability and enable static analysis.

### 2. Dependency Management
- `requirements.txt` clearly lists dependencies.
- Use of Virtual Environment (`venv`) is recommended in `README.md` to avoid system pollution.

### 3. Error Handling
- Use of `HTTPException` for standard HTTP error responses (e.g., 404 Not Found).
- `try-except` blocks in the SDK Client to handle network failures gracefully.

## REST API Design

### 1. Resource-Oriented URLs
Endpoints are designed around resources:
- `/instruments`: Collection of instruments.
- `/orders`: Collection of orders.
- `/orders/{id}`: Specific order resource.

### 2. Standard HTTP Methods & Status Codes
- `GET` for retrieval (200 OK).
- `POST` for creation (201 Created).
- `404 Not Found` for missing resources.
- `422 Unprocessable Entity` (automatic via FastAPI) for validation errors.

### 3. Statelessness
The server is stateless regarding user sessions (mocked user). Each request contains all necessary information (simulated).

### 4. Versioning
API path includes versioning: `/api/v1/...`. This allows future breaking changes without affecting existing clients.

## Simulation Logic
- **Market Orders**: Execute immediately at LTP.
- **Limit Orders**: Validate against LTP. Execute if conditions met, otherwise Queue (PLACED).
- **Portfolio Calculation**: Weighted Average Price calculation on BUY. Verification of holdings on SELL (basic logic implemented).
