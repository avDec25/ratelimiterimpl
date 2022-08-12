install:
	pip install "fastapi[all]"
	pip install "uvicorn[standard]"

run:
	uvicorn main:app --reload