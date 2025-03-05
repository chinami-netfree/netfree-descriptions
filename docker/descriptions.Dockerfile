FROM python:3.12-slim

WORKDIR /app

# התקנת תלויות
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קבצי המקור
COPY api/app.py .
COPY api/summary.py .

# הרצת השרת
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]