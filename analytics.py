import streamlit as st
import altair as alt

def show(source_name, data):
    st.title(f"📈 Analytics - {source_name}")

    # Filter data for the logged-in source name
    data_filter = data[data["Source Name"] == source_name]

    if data_filter.empty:
        st.warning("No data available for this user.")
        return

    # Example: Show top cities by order count
    st.subheader("Top Cities by Order Count")
    city_data = data_filter.groupby("City")["Order ID"].count().reset_index()
    city_data = city_data.sort_values(by="Order ID", ascending=False)  # Sort for better visualization
    city_chart = alt.Chart(city_data).mark_bar().encode(
        x='City',
        y=alt.Y('Order ID', axis=alt.Axis(title='Total Orders')),
        color=alt.Color('City', legend=alt.Legend(title="City")),
        tooltip=['City', 'Order ID']
    ).properties(
        title="Top Cities by Order Count",
        width=600,
        height=400
    )
    st.altair_chart(city_chart, use_container_width=True)

    # Example: Show top services by order count
    st.subheader("Top Services by Order Count")
    service_data = data_filter.groupby("Service Name")["Order ID"].count().reset_index()
    service_data = service_data.sort_values(by="Order ID", ascending=False)  # Sort for better visualization
    service_chart = alt.Chart(service_data).mark_bar().encode(
        x='Service Name',
        y=alt.Y('Order ID', axis=alt.Axis(title='Total Orders')),
        color=alt.Color('Service Name', legend=alt.Legend(title="Service Name")),
        tooltip=['Service Name', 'Order ID']
    ).properties(
        title="Top Services by Order Count",
        width=600,
        height=400
    )
    st.altair_chart(service_chart, use_container_width=True)

    # Example: Show total orders and repeat orders
    st.subheader("Order Statistics")
    total_orders = data_filter['Order ID'].count()
    repeat_orders = data_filter['Order ID'].duplicated().sum()
    repeat_percentage = (repeat_orders / total_orders) * 100 if total_orders > 0 else 0
    st.write(f"**Total Orders:** {total_orders}")
    st.write(f"**Repeat Orders:** {repeat_orders} ({repeat_percentage:.2f}% of total orders)")
