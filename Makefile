all: install scrapy tweepy

install:
	chmod +x simar/process_occurrences.py

scrapy:
	pip3 install scrapy

tweepy:
	pip3 install tweepy
