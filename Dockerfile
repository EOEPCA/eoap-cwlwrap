# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN pip install --upgrade pip setuptools \
    && pip install --prefix=/install .

# Stage 2: Final Image
FROM python:3.11-slim

COPY --from=builder /install /usr/local
COPY src/ src/

CMD ["eoap-cwlwrap", "--help"]
