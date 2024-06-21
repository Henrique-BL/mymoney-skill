install pre-commit:
	@poetry run pre-commit install

run:
	@uvicorn src.main:app --reload
