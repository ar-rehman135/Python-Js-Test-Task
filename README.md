## Backend Setup

1. Navigate to the server directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the backend folder and populate it using `.env.example` as a reference.
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. To run the production server:
   ```bash
   python manage.py collectstatic --no-input
   python manage.py migrate
   gunicorn app.wsgi:application --bind 0.0.0.0:8000
   ```

### Swagger
Visit [http://localhost:8000/api-docs](http://localhost:8000/api-docs) in your browser to see the Swagger documentation.

---