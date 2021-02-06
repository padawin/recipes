#!/bin/bash

rm -r ./out
mkdir -p ./out
cp -r ./src/styles ./src/images ./out/
python3 ./bin/generate_pages.py ./src/ ./recipes/ ./out/
