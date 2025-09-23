import pandas as pd
import psycopg2
from slugify import slugify  # pip install python-slugify
from datetime import datetime

# Path to your Excel file
excel_file = "excel_files/categories2.xlsx"

# Load all sheet names
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names  # detect all sheets automatically

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="cuddlyduddly_db",
    user="cuddlyduddly_user",
    password="strongpassword"
)
cur = conn.cursor()

now = datetime.now()

# Keep track of category slugs inserted in this session
inserted_category_slugs = set()

for sheet in sheet_names:
    # --- Read sheet with header fallback ---
    try:
        df = pd.read_excel(xls, sheet_name=sheet)
    except Exception as e:
        print(f"Skipping sheet '{sheet}' due to read error: {e}")
        continue

    # Skip completely empty sheets
    if df.empty or df.shape[1] == 0:
        print(f"Skipping empty sheet: {sheet}")
        continue

    # --- Insert sheet name into master product table ---
    sheet_slug = slugify(sheet)
    cur.execute(
        """
        INSERT INTO api_masterproduct (name, slug, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (slug) DO NOTHING
        """,
        (sheet, sheet_slug, now, now)
    )

    # --- Determine which column contains categories ---
    if 'Category' in df.columns:
        category_column = 'Category'
    else:
        # fallback to first column, handle sheets without header
        df.columns = [str(c) for c in df.columns]  # ensure column names are strings
        category_column = df.columns[0]

    for cat_name in df[category_column].dropna().unique():
        cat_name = str(cat_name).strip()
        if not cat_name:  # skip empty strings
            continue

        cat_slug = slugify(cat_name)

        # Skip duplicates in this session
        if cat_slug in inserted_category_slugs:
            continue

        # Insert into api_category table, ignore if slug already exists in DB
        cur.execute(
            """
            INSERT INTO api_category (name, slug, description, image_url, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO NOTHING
            """,
            (cat_name, cat_slug, None, None, now, now)
        )

        inserted_category_slugs.add(cat_slug)

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print(f"{len(sheet_names)} sheets processed and categories imported successfully!")
