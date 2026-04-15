FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps

COPY . .

ENV PYTHONPATH=/app

CMD ["sleep", "infinity"]