import streamlit as st
import pandas as pd
import os

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
    df.to_excel(DATA_FILE, index=False)

st.title("🚚 Dispatch Entry System")

df = load_data()

# Summary
st.subheader("📊 Summary Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Dispatches", len(df))
col2.metric("Total Quantity", df["QTY"].sum() if not df.empty else 0)
col3.metric("Total Freight", f"₹{df['FREIGHT AMT'].sum() if not df.empty else 0}")

# Form
with st.form("entry_form"):
    st.subheader("➕ New Dispatch Entry")
    c1, c2 = st.columns(2)
    inv_date = c1.date_input("INV DATE")
    inv_no = c2.text_input("INV No")
    customer = c1.text_input("CUSTOMER")
    salesperson = c2.text_input("SALES PERSON")
    saletype = c1.selectbox("SALE TYPE", ["cash", "credit"])
    product = c2.text_input("PRODUCT")
    model = c1.text_input("MODEL")
    color = c2.text_input("COLOUR")
    qty = c1.number_input("QTY", 0)
    place = c2.text_input("PLACE")
    desp_date = c1.date_input("DESP DATE")
    time = c2.time_input("DESPATCH TIME")
    transport = c1.text_input("TRANSPORT")
    lr = c2.text_input("LR NUMBER")
    vehicle = c1.text_input("VEHICLE NUMBER")
    size = c2.selectbox("VEHICLE SIZE", ["14 feet", "17 feet", "19 feet", "22 feet", "25 feet", "Other"])
    freight = c1.number_input("FREIGHT AMT", 0.0)
    payment_terms = c2.text_input("PAYMENT TERMS")
    payment_status = c1.selectbox("PAYMENT STATUS", ["paid", "pending"])
    remarks = c2.text_input("REMARKS")
    ack_status = c1.selectbox("ACKN STATUS", ["ok", "pending"])
    ack_date = c2.date_input("ACKN SENT DATE")
    ack_by = c1.text_input("ACKN SENT BY")

    submitted = st.form_submit_button("Submit")
    if submitted:
        row = [len(df)+1, inv_date, inv_no, customer, salesperson, saletype, product, model, color, qty,
               place, desp_date, time.strftime('%H:%M'), transport, lr, vehicle, size, freight,
               payment_terms, payment_status, remarks, ack_status, ack_date, ack_by]
        df.loc[len(df)] = row
        save_data(df)
        st.success("Entry added successfully!")

# Table
st.subheader("📋 Dispatch Records")
st.dataframe(df)

# Download
if not df.empty:
    st.download_button("⬇️ Download Excel", df.to_excel(index=False), "dispatch_data.xlsx")


