import time
import requests
import streamlit as st
import pandas  as pd

def reprocess_invoice(invoice_id, org_id):
    url = f"https://api.hyperbots.com/workitems/invoice/v2/{org_id}/reprocess/{invoice_id}"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-length": "0",
        "origin": "https://p2p.hyperbots.com",
        "priority": "u=1, i",
        "referer": "https://p2p.hyperbots.com/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "x-browser-id": "mp4xgr",
        "x-session-id": "1567f684-6fda-492c-98a0-62e91009d3cb"
    }

    cookies = {
        "AMP_MKTG_ffa2a025be": "JTdCJTdE",
        "_gcl_au": "1.1.2037313389.1748846673",
        "_ga": "GA1.1.359934937.1748846674",
        "_ga_LSTNB88YZD": "GS2.1.s1748846674$o1$g1$t1748846697$j37$l0$h0",
        "HYPRBOTS_TOKEN": "eyJraWQiOiJrZXktaWQiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI4N2Y1MGE1OS1iMjRjLTQ1NTAtYmQ2Ny03YzVlYWVjOTc1NWQiLCJicm93c2VyX2lkIjoibXA0eGdyIiwib3JnX2lkIjoiYTAwMTA2ODEtYjVjZi00MjdmLTk0NTEtZWRlODdlZjE5YTFlIiwiZXhwIjoxNzQ5ODEwMTE2LCJpYXQiOjE3NDk4MDY1MTZ9.f8N36CMDkGIVT3xkCM6HyvbdYVVLVyPWv6r83-jf3w9nVVf9oM15XJvuwrO699GrOPh4tbq7DBuzyk9RBvCxW0gurpFUxE3ALsO5u00NJSLuMYQZs6gGOtJCKSX0vUFs9QTRVGJ8y_WC_uRtvfkM7MsTKzqgeoaPKVEmY7SRJ2o",
        "AMP_ffa2a025be": "JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxNzE3ZWNiMi0wMWM2LTQxZDUtODU4Zi1mNDBjNGJhNWZkMWMlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQ5ODA2NDgyMjEwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0OTgwNjU1MTM5MiUyQyUyMmxhc3RFdmVudElkJTIyJTNBNDA3MiUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBNCU3RA=="
    }

    response = requests.put(url, headers=headers, cookies=cookies)

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)


st.title("Invoice Reprocessing")
st.write("Reprocess an invoice by entering its ID and organization ID.")
st.text_input("Invoice ID", key="invoice_id")
st.text_input("Organization ID", key="org_id")
if st.button("Reprocess Invoice"):
    invoice_id = st.session_state.invoice_id
    org_id = st.session_state.org_id
    if invoice_id and org_id:
        reprocess_invoice(invoice_id, org_id)
        st.success("Invoice reprocessing initiated.")
    else:
        st.error("Please provide both Invoice ID and Organization ID.")



def process_invoices(invoice_ids, org_id):
    for invoice_id in invoice_ids:
        try:
            reprocess_invoice(invoice_id, org_id)
            st.success(f"Invoice {invoice_id} reprocessing initiated.")
        except Exception as e:
            st.error(f"Failed to reprocess invoice {invoice_id}: {e}")
    # Placeholder for processing multiple invoices
    st.write("Processing multiple invoices is not implemented yet.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    df_in = pd.read_csv(uploaded_file)
    invoice_list = df_in["id"].astype(str).tolist()
else:
    raw_ids = st.text_area("Invoice IDs")
    invoice_list = [i.strip() for i in raw_ids.splitlines() if i.strip()]

if st.button("Start Processing"):
    org_id = st.session_state.org_id
    if not org_id or not invoice_list:
        st.error("Please fill Org ID, Token and at least one Invoice ID.")
    else:
        progress = st.progress(0)
        results = []
        total = len(invoice_list)
        
        start_time = time.time()
        success_count = 0
        
        for idx, inv in enumerate(invoice_list):
            st.write(f"Processing invoice {idx + 1} of {total}: {inv}")
            success = reprocess_invoice(inv, org_id)
            if success:
                success_count += 1
            progress.progress((idx + 1) / total)

        end_time = time.time()
        st.write(f"Total processing time: {end_time - start_time:.2f} seconds.")






