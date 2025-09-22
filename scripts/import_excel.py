import pandas as pd
import psycopg2
from slugify import slugify  # pip install python-slugify
from datetime import datetime

# Path to your Excel file
excel_file = "excel_files/FIRSTCRY PRODUCT CATEGORY LIST.xls"

# Automatically read all sheet names
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names  # this detects all sheets automatically

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="cuddlyduddly_db",
    user="cuddlyduddly_user",
    password="strongpassword"
)
cur = conn.cursor()

# Insert each sheet name and a slug into your master table
for sheet in sheet_names:
    sheet_slug = slugify(sheet)
    now = datetime.now()
    cur.execute(
        """
        INSERT INTO api_masterproduct (name, slug, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (slug) DO NOTHING
        """,
        (sheet, sheet_slug, now, now)
    )

conn.commit()
cur.close()
conn.close()

print(f"{len(sheet_names)} sheet names stored in master table.")
