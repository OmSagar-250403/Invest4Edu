# Project: Report Card Generator and LinkedIn Profile Scraper

This project consists of two Python scripts: 
1. **Report Card Generator (`code_01.py`)**
2. **LinkedIn Profile Scraper (`code_02.py`)**

## Overview

### Report Card Generator (`code_01.py`)
This script generates a PDF report card for a student based on their scores provided in an Excel file (`Student_Scores.xlsx`). The output is stored as individual PDF files for each student in the `Output` folder.

### LinkedIn Profile Scraper (`code_02.py`)
This script logs into LinkedIn, searches for profiles based on a query, scrapes user data (names and profile information) from a specified number of pages, and saves the data into a CSV file in the `Output` folder.

---

## Setup Instructions

### Prerequisites
1. **Python 3.8+**
2. Install required Python libraries using:
   ```bash
   pip install pandas reportlab selenium beautifulsoup4


project_folder/
│
├── src/
│   ├── code_01.py          # Report Card Generator script
│   ├── code_02.py          # LinkedIn Scraper script
│
├── Student_Scores.xlsx     # Input file for report card generation
├── Output/                 # Output folder for generated files
│   ├── report_card_*.pdf   # PDF report cards
│   ├── profiles.csv        # Scraped LinkedIn profile data
│
└── README.md               # Project documentation
