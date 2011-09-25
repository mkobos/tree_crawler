#!/bin/bash

## epydoc hangs for some reason if the `src.run_tests` and `src.test` paths are not excluded
#epydoc concurrent_tree_crawler -o ../epydoc --graph all $1 $2 $3

## do not make documentation for tests and the versioning function
epydoc concurrent_tree_crawler -o docs-api --graph all --exclude test --exclude concurrent_tree_crawler.common.version $1 $2 $3
