# Library Management API

This is a simple Flask-based RESTful API for managing a library's book collection. The API allows users to add, list, search, update, and delete books. This project is an assignment served as a part of the CSAI-203 (Introduction to Software Engineering) course in Zewail UST.

## Features
- Add new books
- List all books
- Search books by author, published year, or genre
- Delete books by ISBN
- Update book details
- Swagger UI documentation

## Dependencies
- Docker
- Python 3.9+

## Installation and Setup

### Local Development
1. Clone the repository
```bash
git clone https://github.com/0x3mr/libAPI
cd libAPI
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

### Docker Deployment
1. Build the Docker image
```bash
docker build -t libAPI .
```

2. Run the Docker container
```bash
docker run -p 5000:5000 libAPI
```

## API Endpoints

### Add a Book
- **POST** `/books`
- Required fields: `title`, `author`, `publishedYear`, `isbn`
- Optional field: `genre`

### List/Search Books
- **GET** `/books`
- Optional query parameters: `author`, `publishedYear`, `genre`

### Delete a Book
- **DELETE** `/books/<isbn>`

### Update a Book
- **PUT** `/books/<isbn>`

## API Documentation
Swagger UI is available at `/api-docs`

## Postman Collection
Link: TBD.

## Notes
- Data is stored in a local `books.json` file

## Project Structure
```
libAPI/
│
├── app.py                   # Main Flask application
├── books.json               # JSON file for storing book data
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── postman_collection.json  # Postman API collection
│
├── static/
│   └── swagger.json         # API documentation
│
├── LICENSE                  # MIT License
└── README.md                # Project outline
```
## [License](LICENSE)
