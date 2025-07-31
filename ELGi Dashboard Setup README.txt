
ELGi Enquiries Dashboard
========================

This project is a Streamlit-based dashboard that visualizes enquiry data received by ELGi. 
It helps understand trends across countries, industries, equipment types, and time.

Features
--------

- View total enquiries, countries involved, and top equipment
- Filter data by date, country, and industry group
- Visualizations include:
  - Enquiries by Country (bar + pie chart)
  - Industry-wise breakdown
  - Equipment type interest (pie)
  - Monthly trends over time
- Option to view the filtered raw data

Tech Stack
----------

- Python
- Streamlit (for the interactive dashboard)
- Pandas (for data manipulation)
- Plotly Express (for interactive charts)
- Excel (as the data source)

Project Structure
-----------------

elgi-dashboard/
├── dashboard.py       <- main Streamlit app
├── ELGi Website Entries 2024.xlsx  <- input Excel file
└── README.txt

How to Run
----------

1. Install the requirements:

   pip install streamlit pandas plotly openpyxl

2. Prepare Your Excel File:

   - Name: ELGi Website Entries 2024.xlsx
   - Columns required:
     - Entry Date
     - Country
     - Industry
     - Equipment Type
   - Place the file in the same directory as your Python file.

3. Run the Dashboard:

   streamlit run dashboard.py

   Once running, a browser tab should open with your dashboard UI.

Notes & Logic
-------------

- Grouped Industry was created manually using keyword matching to cluster similar industry types 
  (like 'agri' and 'fmcg' into 'Consumer Sector').
- The dashboard filters are dynamic — charts only show filtered data.
- Missing values in dates or categories are handled using .dropna() or default labels like "Unknown".

Author
------

Pranav Menon
Final-year student working on data visualization using Python.
