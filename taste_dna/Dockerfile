FROM python:3.9-slim-buster

# Set working directory
WORKDIR /home/taste_dna

# Copy requirements
COPY --chown=taste_dna Pipfile Pipfile.lock taste-dna-python/

ENV PATH="/home/taste_dna/.local/bin:${PATH}"
# Install dependencies
RUN pip install pipenv && \
    cd taste-dna-python && \
    pipenv install --dev --system

# Copy project files
COPY --chown=taste_dna . taste-dna-python

EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
