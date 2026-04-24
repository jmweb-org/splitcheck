# Check splits from inside a container by mounting them:
#
#   docker build -t splitcheck .
#   docker run --rm -v "$PWD:/w" -w /w splitcheck check train.csv test.csv --on text
#
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/jmweb-org/splitcheck"
LABEL org.opencontainers.image.description="Detect row overlap and leakage between dataset splits."
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir .

ENTRYPOINT ["splitcheck"]
CMD ["--help"]
