FROM python:3.11.4 as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/api/src"

WORKDIR /api

# Install dependencies
COPY pyproject.toml poetry.lock /api/
RUN pip install poetry && poetry lock --no-update && poetry install --no-root

# Verify Uvicorn installation
RUN poetry run uvicorn --version

# Copy project files
COPY . .

# Expose the port
EXPOSE 8080

# Run the server
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]