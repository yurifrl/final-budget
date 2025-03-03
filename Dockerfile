# Base image
FROM python as base


RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --dev

# Dev environment
FROM base as dev
RUN pip install go-task-bin
RUN apt-get update && apt-get install -y fish \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment and ensure its binaries are in PATH
COPY --from=base /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . .
CMD ["fish"]

# Prod environment
FROM base as prod
COPY . .
CMD ["python", "main.py"]
