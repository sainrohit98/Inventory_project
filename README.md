# Inventory Management System API
This project is a backend API for a simple Inventory Management System using Django Rest Framework.

### Features
 CRUD operations for inventory items 
JWT authentication
Redis caching for improved performance
PostgreSQL database
Logging for debugging and monitoring
Unit tests


Set up the PostgreSQL database and update the DATABASES configuration in inventory_project/settings.py.
Install and start Redis server
---

## Setup


1. Clone the repository:

```bash
git clone https://github.com/sainrohit98/Inventory_project.git

```


2. Create and activate a virtual environment:
python -m venv venv
`venv\Scripts\activate`

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```


## API Endpoints

POST /api/token/: Obtain JWT token
POST /api/token/refresh/: Refresh JWT token
GET /api/items/: List all items
POST /api/items/: Create a new item
GET /api/items/{id}/: Retrieve an item
PUT /api/items/{id}/: Update an item
DELETE /api/items/{id}/: Delete an item


### Authentication Endpoints

#### 1. Obtain JWT Token
- **Endpoint**: `POST /api/token/`
- **Description**: Obtain a JWT token using username and password.

**Request**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

#### 2. Refresh JWT Token
- **Endpoint**: `POST /api/token/refresh/`
- **Description**: Refresh the JWT token using the refresh token.

**Request**:
```json
{
  "refresh": "your_refresh_token"
}
```

**Response**:
```json
{
  "access": "your_new_access_token"
}
```

### Inventory Item Endpoints

#### 1. List All Items
- **Endpoint**: `GET /api/items/`
- **Description**: Retrieve a list of all inventory items.
- **Authentication**: Requires a valid JWT token.

**Example Request**:
```bash
GET /api/items/
Authorization: Bearer your_access_token
```

**Response**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "A high-performance laptop.",
    "quantity": 10,
    "created_at": "2023-09-26T10:00:00Z",
    "updated_at": "2023-09-26T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Mouse",
    "description": "Wireless mouse.",
    "quantity": 50,
    "created_at": "2023-09-26T10:05:00Z",
    "updated_at": "2023-09-26T10:05:00Z"
  }
]
```

#### 2. Create a New Item
- **Endpoint**: `POST /api/items/`
- **Description**: Create a new inventory item.
- **Authentication**: Requires a valid JWT token.

**Request**:
```json
{
  "name": "Keyboard",
  "description": "Mechanical keyboard.",
  "quantity": 30
}
```

**Response**:
```json
{
  "id": 3,
  "name": "Keyboard",
  "description": "Mechanical keyboard.",
  "quantity": 30,
  "created_at": "2023-09-26T10:10:00Z",
  "updated_at": "2023-09-26T10:10:00Z"
}
```

#### 3. Retrieve a Single Item
- **Endpoint**: `GET /api/items/{id}/`
- **Description**: Retrieve the details of a specific inventory item by its ID.
- **Authentication**: Requires a valid JWT token.

**Example Request**:
```bash
GET /api/items/1/
Authorization: Bearer your_access_token
```

**Response**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "A high-performance laptop.",
  "quantity": 10,
  "created_at": "2023-09-26T10:00:00Z",
  "updated_at": "2023-09-26T10:00:00Z"
}
```

#### 4. Update an Item
- **Endpoint**: `PUT /api/items/{id}/`
- **Description**: Update an existing inventory item by its ID.
- **Authentication**: Requires a valid JWT token.

**Request**:
```json
{
  "name": "Laptop",
  "description": "A high-performance gaming laptop.",
  "quantity": 8
}
```

**Response**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "A high-performance gaming laptop.",
  "quantity": 8,
  "created_at": "2023-09-26T10:00:00Z",
  "updated_at": "2023-09-26T12:00:00Z"
}
```

#### 5. Delete an Item
- **Endpoint**: `DELETE /api/items/{id}/`
- **Description**: Delete an existing inventory item by its ID.
- **Authentication**: Requires a valid JWT token.

**Example Request**:
```bash
DELETE /api/items/1/
Authorization: Bearer your_access_token
```

**Response**:
```json
{
  "message": "Item deleted successfully."
}
```

---

### Running Tests
To run the unit tests:
```bash
python manage.py test
```

# Logging
Logs are stored in debug.log in the project root directory.
# Redis Caching
The application uses Redis for caching frequently accessed items. Make sure Redis is running on your system before starting the application.