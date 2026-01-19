FROM python:3.11-slim

WORKDIR /app

# Install build deps and pip requirements
RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		build-essential \
		gcc \
		libpq-dev \
		pkg-config \
		libssl-dev \
		ca-certificates \
		curl \
		git \
		rustc \
		cargo && \
	rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PORT=5000

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
