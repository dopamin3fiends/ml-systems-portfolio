# Makefile for managing the ML Systems Portfolio project

.PHONY: install clean run test

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up temporary files and directories
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -exec rm -f {} +

# Run the backend application
run:
	python src/backend/app.py

# Run unit tests
test:
	pytest tests/unit

# Run integration tests
integration:
	pytest tests/integration

# Build Docker image
docker-build:
	docker build -t ml-systems-portfolio infra/docker/

# Run Docker container
docker-run:
	docker run -p 5000:5000 ml-systems-portfolio

# Deploy application using ETL script
deploy:
	python src/scripts/deploy.py

# Execute ETL process
etl:
	python src/scripts/etl.py

# Run Jupyter notebook for exploration
notebook:
	jupyter notebook notebooks/exploration.ipynb