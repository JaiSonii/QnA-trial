# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed
# Copy project definition
COPY pyproject.toml .

# Install dependencies
# FIX: Added 'pydantic-settings' to this line
RUN pip install --no-cache-dir fastapi[standard] uvicorn sqlmodel python-jose[cryptography] bcrypt==3.2.2 passlib[bcrypt] python-multipart langchain langchain-openai httpx alembic pydantic-settings

# Copy the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]