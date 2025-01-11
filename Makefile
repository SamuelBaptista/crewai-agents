.PHONY: lint app login deploy clear

CODEARTIFACT_DOMAIN := repense
CODEARTIFACT_OWNER := 329495585553

login:
	$(eval CODEARTIFACT_AUTH_TOKEN := $(shell aws codeartifact get-authorization-token --domain $(CODEARTIFACT_DOMAIN) --domain-owner $(CODEARTIFACT_OWNER) --query authorizationToken --output text))
	poetry config http-basic.repense-ai aws $(CODEARTIFACT_AUTH_TOKEN)
	poetry config http-basic.repense-db aws $(CODEARTIFACT_AUTH_TOKEN)

lint:
	black src
	flake8 src

clear:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

app:
	streamlit run app.py