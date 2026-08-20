FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_RETRIES=10
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

FROM python:3.12-slim
RUN useradd --create-home appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
EXPOSE 8501
# Streamlit exposes a built-in health endpoint at /_stcore/health — use it
# for a readiness/liveness probe when this image is deployed.
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]