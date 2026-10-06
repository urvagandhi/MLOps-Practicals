# ==========================================
# Stage 1: Builder (Build Python wheels)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# ==========================================
# Stage 2: Final Image (Clean runtime)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# Copy Python wheels from builder and install cleanly
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application files
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
