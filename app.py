import streamlit as st
import pandas as pd
import os
import io
import xlsxwriter

DATA_FILE = "dispatch_data.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    columns = [
        "S.No", "INV DATE", "INV No", "CUSTOMER", "SALES PERSON", "SALE TYPE", "PRODUCT", "MODEL",
        "COLOUR", "QTY", "PLACE", "DESP DATE", "DESPATCH TIME", "TRANSPORT", "LR NUMBER",
        "VEHICLE NUMBER", "VEHICLE SIZE", "FREIGHT AMT", "PAYMENT TERMS", "PAYMENT STATUS",
        "REMARKS", "ACKN STATUS", "ACKN SENT DATE", "ACKN SENT BY"
    ]
    pd.DataFrame(columns=columns).to_csv(DATA_FILE, index=False)

# Load existing data
df = pd.read_csv(DATA_FILE)

st.title("📦 Dispatch Entry Form")

with st.form("dispatch_form"):
    inv_date = st.date_input("INV DATE")
    inv_no = st.number_input("INV No", min_value=1, step=1, format="%d")
    inv_no = str(int(inv_no))  # Convert to string

    customer = st.text_input("CUSTOMER")
    sales_person = st.text_input("SALES PERSON")
    sale_type = st.selectbox("SALE TYPE", ["Cash", "Credit"])
    product = st.text_input("PRODUCT")
    model = st.text_input("MODEL")
    colour = st.text_input("COLOUR")
    qty = st.number_input("QTY", min_value=0, step=1)
    place = st.text_input("PLACE")
    desp_date = st.date_input("DESP DATE")
    desp_time = st.time_input("DESPATCH TIME")
    transport = st.text_input("TRANSPORT")
    lr_number = st.text_input("LR NUMBER")
    vehicle_number = st.text_input("VEHICLE NUMBER")
    vehicle_size = st.selectbox("VEHICLE SIZE", ["Small", "Medium", "Large"])
    freight_amt = st.number_input("FREIGHT AMT", min_value=0.0)
    payment_terms = st.text_input("PAYMENT TERMS")
    payment_status = st.selectbox("PAYMENT STATUS", ["Paid", "Unpaid", "Partial"])
    remarks = st.text_area("REMARKS")
    ackn_status = st.selectbox("ACKN STATUS", ["Pending", "Sent"])
    ackn_sent_date = st.date_input("ACKN SENT DATE")
    ackn_sent_by = st.text_input("ACKN SENT BY")

    submitted = st.form_submit_button("✅ Save Entry")
    refresh = st.form_submit_button("🔄 Refresh Form")

    if refresh:
        st.experimental_rerun()

    if submitted:
        if inv_no.strip() == "":
            st.warning("Invoice Number is required to save.")
        else:
            if inv_no in df["INV No"].astype(str).values:
                index = df[df["INV No"].astype(str) == inv_no].index[0]
                df.loc[index] = [
                    index + 1, inv_date, inv_no, customer, sales_person,
                    sale_type, product, model, colour, qty, place, desp_date,
                    desp_time, transport, lr_number, vehicle_number,
                    vehicle_size, freight_amt, payment_terms, payment_status,
                    remarks, ackn_status, ackn_sent_date, ackn_sent_by
                ]
                st.success(f"✅ Updated entry for INV No {inv_no}.")
            else:
                new_entry = {
                    "S.No": len(df) + 1,
                    "INV DATE": inv_date,
                    "INV No": inv_no,
                    "CUSTOMER": customer,
                    "SALES PERSON": sales_person,
                    "SALE TYPE": sale_type,
                    "PRODUCT": product,
                    "MODEL": model,
                    "COLOUR": colour,
                    "QTY": qty,
                    "PLACE": place,
                    "DESP DATE": desp_date,
                    "DESPATCH TIME": desp_time,
                    "TRANSPORT": transport,
                    "LR NUMBER": lr_number,
                    "VEHICLE NUMBER": vehicle_number,
                    "VEHICLE SIZE": vehicle_size,
                    "FREIGHT AMT": freight_amt,
                    "PAYMENT TERMS": payment_terms,
                    "PAYMENT STATUS": payment_status,
                    "REMARKS": remarks,
                    "ACKN STATUS": ackn_status,
                    "ACKN SENT DATE": ackn_sent_date,
                    "ACKN SENT BY": ackn_sent_by
                }

                new_row_df = pd.DataFrame([new_entry], columns=df.columns)

                if df.empty:
                    df = new_row_df
                else:
                    df = pd.concat([df, new_row_df], ignore_index=True)

                st.success(f"✅ Saved new entry for INV No {inv_no}.")
            df.to_csv(DATA_FILE, index=False)

# ------------------------
# 🔍 Load/Delete Section
# ------------------------
st.subheader("🔍 Load or Delete Entry")
load_inv = st.text_input("Enter Invoice No to Load or Delete")
col1, col2 = st.columns(2)

if col1.button("📂 Load Entry"):
    entry = df[df["INV No"].astype(str) == load_inv.strip()]
    if not entry.empty:
        st.write("### Entry Found:")
        st.dataframe(entry)
    else:
        st.warning("No entry found with that Invoice No.")

if col2.button("🗑️ Delete Entry"):
    if load_inv.strip() in df["INV No"].astype(str).values:
        df = df[df["INV No"].astype(str) != load_inv.strip()].reset_index(drop=True)
        df["S.No"] = range(1, len(df) + 1)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"🗑️ Entry with Invoice No {load_inv.strip()} deleted.")
    else:
        st.warning("Invoice No not found.")

# ------------------------
# 📥 Download as Excel
# ------------------------
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dispatch Data')
    return output.getvalue()

st.subheader("📤 Export Data")
excel_data = to_excel(df)
st.download_button(
    label="📥 Download Full Data as Excel",
    data=excel_data,
    file_name='dispatch_data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
