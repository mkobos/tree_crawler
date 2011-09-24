#!/bin/bash

cd src

## epydoc hangs for some reason if the `src.run_tests` and `src.test` paths are not excluded
#epydoc . -o ../epydoc --graph all $1 $2 $3

## do not make documentation for tests
epydoc . -o ../docs-api --graph all --exclude test $1 $2 $3
