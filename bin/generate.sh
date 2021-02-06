#!/bin/bash

if [ "$1" == "all" ]; then
	rm -r ./out
	mkdir -p ./out
fi

if [ "$1" == "all" ] || [ "$1" == "content" ]; then
	cp -r ./src/styles ./out/
	python3 ./bin/generate_pages.py ./src/ ./recipes/ ./out/
fi
if [ "$1" == "all" ] || [ "$1" == "images" ]; then
	cp -r ./src/images ./out/
	python3 ./bin/generate_images.py ./src/ ./recipes/ ./out/
fi
