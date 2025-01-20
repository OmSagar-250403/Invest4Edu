from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os

# Read the data from the Excel file
file_path = "Student_Scores.xlsx"  # Update this path if necessary
try:
    data = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Validate the data
required_columns = ['Roll No.', 'Name']
if not all(col in data.columns for col in required_columns):
    print("Error: Missing required columns ('Roll No.' and 'Name') in the Excel file.")
    exit()

# Ensure score columns are numeric
try:
    score_columns = data.columns[2:]  # All columns from Sub-1 onward
    data[score_columns] = data[score_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
except Exception as e:
    print(f"Error processing score columns: {e}")
    exit()

# Calculate Total and Average Scores
data['Total'] = data[score_columns].sum(axis=1)
data['Average'] = data[score_columns].mean(axis=1)

# Create a directory to store the PDF report cards
output_dir = "Report_Cards"
os.makedirs(output_dir, exist_ok=True)

# Function to generate a PDF report card for a student
def generate_pdf(student_data):
    roll_no = student_data['Roll No.']
    name = student_data['Name']
    total = student_data['Total']
    average = student_data['Average']
    subjects = student_data[score_columns].to_dict()  # All subjects with scores
    
    # PDF file name
    pdf_file = os.path.join(output_dir, f"report_card_{roll_no}.pdf")
    
    # Create a PDF document
    pdf = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []
    
    # Styles for the document
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    # Add title
    title = Paragraph(f"Report Card: {name}", title_style)
    elements.append(title)
    
    # Add student details
    elements.append(Paragraph(f"Roll No: {roll_no}", normal_style))
    elements.append(Paragraph(f"Name: {name}", normal_style))
    elements.append(Paragraph(f"Total Score: {total}", normal_style))
    elements.append(Paragraph(f"Average Score: {average:.2f}", normal_style))
    
    # Add a table for subject-wise scores
    table_data = [['Subject', 'Score']] + [[subject, score] for subject, score in subjects.items()]
    table = Table(table_data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    
    # Footer
    elements.append(Paragraph("This is a system-generated report card.", normal_style))
    
    # Build the PDF
    try:
        pdf.build(elements)
        print(f"Report card generated for {name}: {pdf_file}")
    except Exception as e:
        print(f"Error generating report card for {name}: {e}")

# Prompt the user to enter a Roll Number
try:
    roll_no_input = int(input("Enter the Roll Number of the student to generate the report card: "))
    student_data = data[data['Roll No.'] == roll_no_input]
    if student_data.empty:
        print(f"Error: No student found with Roll Number {roll_no_input}.")
    else:
        generate_pdf(student_data.iloc[0])  # Pass the first matching row as a series
except ValueError:
    print("Error: Please enter a valid Roll Number.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
