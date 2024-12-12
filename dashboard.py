import streamlit as st
import pandas as pd

def show(source_name, data):
    st.title(f"Gomechanic Dashboard - {source_name}")

    # Check if the necessary columns exist in the data
    required_columns = ["Source Name", "Order ID", "City", "Service Name", "Car Name", "Customer Name", "Car Model",
                        "Car Odometer", "Car No", "Mobile No", "Invoice Link", "Delivered Date"]
    if not all(col in data.columns for col in required_columns):
        st.error("Some required columns are missing in the data.")
        return

    # Filter data for the logged-in source name
    data_filter = data[data["Source Name"] == source_name]

    if data_filter.empty:
        st.warning("No data available for this user.")
        return

    # Display basic stats
    st.subheader(f"**Total Orders:** {data_filter['Order ID'].count()}")
    st.subheader(f"**Total Repeat Orders:** {data_filter['Order ID'].duplicated().sum()}")
    st.subheader(f"**Working Cities:** {data_filter['City'].nunique()}")

    # Search for an Order ID
    order_ids = data_filter["Order ID"].unique()
    order_id_search = st.selectbox("Search Order ID", options=["Select an Order ID"] + list(order_ids))

    if order_id_search:
        # Check if the entered Order ID exists
        order_details = data_filter[data_filter["Order ID"] == order_id_search]

        if not order_details.empty:
            st.subheader(f"**Order Details for Order ID: {order_id_search}**")
            # Show the detailed information
            for index, row in order_details.iterrows():
                st.write(f"**Car Name:** {row['Car Name']}")
                st.write(f"**Customer Name:** {row['Customer Name']}")
                st.write(f"**Delivered Date:** {row['Delivered Date']}")
                st.write(f"**Car Odometer:** {row['Car Odometer']}")
                st.write(f"**Car No:** {row['Car No']}")
                st.write(f"**Mobile No:** {row['Mobile No']}")
                st.write(f"**Service Name:** {row['Service Name']}")

                # Display the Invoice Download Button
                if pd.notna(row['Invoice Link']):
                    st.download_button(
                        label="Download Invoice",
                        data=row['Invoice Link'],  # Assuming this is a file link
                        file_name=f"Invoice_{order_id_search}.pdf",  # Adjust the file extension based on the file type
                        mime="application/pdf",  # Change MIME type based on file format
                        key=f"download_button_{order_id_search}_{index}"  # Unique key for each button
                    )
        else:
            st.warning(f"No details found for Order ID: {order_id_search}")
