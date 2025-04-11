FROM python:3.9
WORKDIR /app
COPY app.py .
COPY templates/ templates/
RUN pip install flask openai python-dotenv
CMD ["python", "app.py"]

