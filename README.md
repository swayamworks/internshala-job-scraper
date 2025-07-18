# Internshala Job Scraper 🕵️‍♂️

A Python script using Selenium to scrape work-from-home internship listings in Mumbai from [Internshala](https://internshala.com).

## Features

- Scrapes job title, company, stipend, duration, and application link
- Automatically paginates through all pages
- Skips duplicates and missing data
- Saves output to `internshala_jobs.csv`

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver

## Setup

```bash
pip install selenium pandas
