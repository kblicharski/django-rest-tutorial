#!/bin/bash
autopep8 -ir -j 0 -p 1000 -a --exclude **migrations** --max-line-length 100 .
isort -rc .
pycodestyle --statistics --count --format=pylint --max-line-length=100 .