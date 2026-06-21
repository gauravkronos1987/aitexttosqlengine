FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY ./src ./src

RUN pip install -e .

COPY . .

EXPOSE 8501

CMD ["streamlit","run","src/aitexttosqlengine/app.py","--server.port=8501","--server.address=0.0.0.0"]