FROM python:3.11-slim
WORKDIR /app

COPY . .
RUN apt update && apt install -y git
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "-m", "kpoisk_bot"]
