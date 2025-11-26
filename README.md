# simple-python-chatbot-6506-6515

Django REST backend for a simple chatbot. Provides:
- GET /api/health/ — health check
- POST /api/chat/ — send a user message and receive an assistant reply
- GET /api/conversations/ — list conversations (optional)
- GET /api/conversations/<id>/ — get a conversation and its messages

Docs:
- Swagger UI: /docs
- ReDoc: /redoc

Setup and migrations:
1. Install dependencies:
   pip install -r chatbot_backend/requirements.txt

2. Run migrations (required after these model additions):
   cd chatbot_backend
   python manage.py makemigrations
   python manage.py migrate

3. Run server:
   python manage.py runserver 0.0.0.0:3001