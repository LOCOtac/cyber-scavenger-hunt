FROM python:3.9
WORKDIR /app
COPY app.py .
COPY templates/ templates/
RUN pip install flask openai python-dotenv
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]


