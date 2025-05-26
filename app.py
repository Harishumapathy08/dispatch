import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

st.set_page_config(layout="wide")
DATA_FILE = 'data/dispatch_data.xlsx'
os.makedirs("data", exist_ok=True)

columns = [
    "S.No", "INV DATE", "INV No", "CUSTOMER", "SALES PERSON", "SALE TYPE", "PRODUCT", "MODEL",
    "COLOUR", "QTY", "PLACE", "DESP DATE", "DESPATCH TIME", "TRANSPORT", "LR NUMBER",
    "VEHICLE NUMBER", "VEHICLE SIZE", "FREIGHT AMT", "PAYMENT TERMS", "PAYMENT STATUS",
    "REMARKS", "ACKN STATUS", "ACKN SENT DATE", "ACKN SENT BY"
]

def load_data():
    return pd.read_excel(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame(columns=columns)

def save_data(df):
    df.to_excel(DATA_FILE, index=False, engine='openpyxl')

df = load_data()

# Style
st.markdown("""
    <style>
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stDateInput>div>div>input,
    .stTimeInput>div>div>input {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    .stButton>button {
        padding: 10px 20px;
        background-color: #1a73e8;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0f5fc0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚚 Dispatch Entry System")

# Summary
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Dispatches", len(df))
col2.metric("Total Quantity", df["QTY"].sum() if not df.empty else 0)
col3.metric("Total Freight", f"₹{df["FREIGHT AMT"].sum() if not df.empty else 0}")

# Add Entry Form
st.subheader("➕ Add Dispatch Record")
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    inv_date = col1.date_input("INV DATE")
    inv_no = col2.text_input("INV No")
    customer = col1.text_input("CUSTOMER")
    salesperson = col2.text_input("SALES PERSON")
    saletype = col1.selectbox("SALE TYPE", ["cash", "credit"])
    product = col2.text_input("PRODUCT")
    model = col1.text_input("MODEL")
    color = col2.text_input("COLOUR")
    qty = col1.number_input("QTY", 0)
    place = col2.text_input("PLACE")
    desp_date = col1.date_input("DESP DATE")
    time = col2.time_input("DESPATCH TIME")
    transport = col1.text_input("TRANSPORT")
    lr = col2.text_input("LR NUMBER")
    vehicle = col1.text_input("VEHICLE NUMBER")
    size = col2.selectbox("VEHICLE SIZE", ["14 feet", "17 feet", "19 feet", "22 feet", "25 feet", "Other"])
    freight = col1.number_input("FREIGHT AMT", 0.0)
    payment_terms = col2.text_input("PAYMENT TERMS")
    payment_status = col1.selectbox("PAYMENT STATUS", ["paid", "pending"])
    remarks = col2.text_input("REMARKS")
    ack_status = col1.selectbox("ACKN STATUS", ["ok", "pending"])
    ack_date = col2.date_input("ACKN SENT DATE")
    ack_by = col1.text_input("ACKN SENT BY")

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_row = [len(df)+1, inv_date, inv_no, customer, salesperson, saletype, product, model, color, qty,
                   place, desp_date, time.strftime('%H:%M'), transport, lr, vehicle, size, freight,
                   payment_terms, payment_status, remarks, ack_status, ack_date, ack_by]
        df.loc[len(df)] = new_row
        save_data(df)
        st.success("✅ Entry added successfully!")
        st.experimental_rerun()

# View & Delete Records
st.subheader("📋 Dispatch Records")

if not df.empty:
    for i, row in df.iterrows():
        with st.expander(f"🔎 Record {int(row['S.No'])} - {row['CUSTOMER']}"):
            cols = st.columns(2)
            for j, col in enumerate(columns[1:]):
                with cols[j % 2]:
                    st.write(f"**{col}:** {row[col]}")
            if st.button(f"🗑 Delete Record {int(row['S.No'])}", key=f"delete_{i}"):
                df = df[df["S.No"] != row["S.No"]]
                df.reset_index(drop=True, inplace=True)
                df["S.No"] = df.index + 1
                save_data(df)
                st.success("🗑 Record deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No dispatch records available.")

# Excel Download
if not df.empty:
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    st.download_button(
        label="⬇️ Download Excel",
        data=buffer,
        file_name="dispatch_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )







