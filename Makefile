all: install scrapy tweepy

install:
	chmod +x simar/process_occurrences.py
	chmod +x run_simar.sh

scrapy:
	pip3 install scrapy

tweepy:
	pip3 install tweepy
