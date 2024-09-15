FROM python:3.9

WORKDIR .

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
