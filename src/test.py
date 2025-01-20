from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os

# Read the data from the Excel file
file_path = "..\Student_Scores.xlsx"  # Update this path if necessary
try:
    data = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

print(data.columns[0])