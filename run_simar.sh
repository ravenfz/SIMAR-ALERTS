#!/bin/bash

cd simar/
rm roturas.json
python3 simar_crawler.py
python3 process_occurrences.py

