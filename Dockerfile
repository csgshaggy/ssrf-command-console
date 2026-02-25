# ============================
# Stage 1 — Build environment
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ============================
# Stage 2 — Runtime environment
# ============================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application AFTER the FROM line
COPY app ./app
COPY logs ./logs
COPY scripts ./scripts
COPY dashboard ./dashboard

# Ensure logs directory exists
RUN mkdir -p logs

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
