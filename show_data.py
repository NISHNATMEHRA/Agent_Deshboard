import streamlit as st

def show(source_name, data):
    st.title("📊 Show Data")
    data_filter = data[data["Source Name"] == source_name]

    required_columns = ["Source Name", "Order ID", "City", "Service Name", "Car Name", "Customer Name",
                        "Car Odometer", "Car No", "Mobile No", "Delivered Date"]

    # Filter the data to keep only the required columns
    data_filter = data_filter[required_columns]

    if data_filter.empty:
        st.warning(f"No data found for source: **{source_name}**")
        return

    # Dropdown to select search type: City or All Data
    un_city = data_filter["City"].unique()
    search_type = st.selectbox("Search by", options=["Select an option", "all City"] + list(un_city))

    if search_type == "all City":
        st.write(f"Showing data for all cities.")
        st.write(data_filter)

    elif search_type in un_city:
        data_city = data_filter[data_filter["City"] == search_type]
        st.write(f"Showing data for city: **{search_type}**")
        st.write(data_city)
