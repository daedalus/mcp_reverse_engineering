FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY pyproject.toml README.md .

RUN pip install --no-cache-dir -e .

ENV MCP_RE_WORKSPACE=/workspace
ENV MCP_RE_TIMEOUT=30

RUN mkdir -p /workspace

EXPOSE 8000

ENTRYPOINT ["mcp-re"]
CMD ["--help"]
