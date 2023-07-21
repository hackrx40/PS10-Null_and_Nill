import os
import requests
import pdfplumber

invoice_pdf = ''
os.system(f'ocrmypdf {invoice_pdf} output.pdf --force-ocr')

data = []

with pdfplumber.open("ouptut.pdf") as pdf:
    for i in range(len(pdf.pages)):
        data.append(pdf.pages[i].extract_text(x_tolerance = 2))

os.remove("output.pdf")


file1.open("","a")
file1.writelines(data)
file1.close()

