.PHONY: antlr-gen antlerate_python
antlr-generate_python: ## Build parser for Python3
	docker build -t antlr "$(shell pwd)"/
	docker run -u $(shell id -u):$(shell id -g) -v $(shell pwd)/antlr/:/antlr antlr -visitor -no-listener -Dlanguage=Python3 -o /antlr/target/python /antlr/PC.g4;
	mkdir -p ./libs
	mv ./antlr/target/python/* ./libs