FROM python:3.12.0a1-alpine3.16

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./receiber.py"]