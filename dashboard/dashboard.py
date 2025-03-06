import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

all_df = pd.read_csv("all_df.csv")

# Judul Dashboard
st.header("Analisis Produk & Metode Pembayaran :sparkles:")

tab1, tab2, tab3 = st.tabs(
    ["💳 Metode Pembayaran", "📦 Analisis Produk", "🌍 Geospatial Analysis"]
)

with tab1:
    st.header("Analisis Metode Pembayaran")

    sum_order_payments_df = (
        all_df.groupby("payment_type")
        .order_id.nunique()
        .sort_values(ascending=False)
        .reset_index()
    )
    sum_order_payments_df = sum_order_payments_df.rename(
        columns={"order_id": "quantity"}
    )

    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox(
            "Urutkan berdasarkan",
            ["Jumlah Transaksi", "Nama"],
            key="payment_sort",
        )
    with col2:
        sort_order = st.radio(
            "Urutan",
            ["Dari terkecil", "Dari terbesar"],
            horizontal=True,
            key="payment_order",
        )

    if sort_by == "Jumlah Transaksi":
        sort_column = "quantity"
    else:
        sort_column = "payment_type"

    ascending = True if sort_order == "Dari terkecil" else False
    sorted_df = sum_order_payments_df.sort_values(by=sort_column, ascending=ascending)

    fig, ax = plt.subplots(figsize=(16, 6))

    sns.barplot(
        x="payment_type",
        y="quantity",
        data=sorted_df.head(5),
        palette="Blues_d",
        hue="payment_type",
    )
    ax.set_title("Jumlah Metode Pembayaran yang Digunakan")
    ax.set_ylabel("Jumlah Transaksi")
    ax.set_xlabel("Metode Pembayaran")

    st.pyplot(fig)

    # Tampilkan data frame
    st.subheader("Data Metode Pembayaran")
    with st.expander("📋 Lihat Data Lengkap Metode Pembayaran"):
        st.dataframe(sum_order_payments_df)

with tab2:
    st.header("Analisis Produk")

    sum_orders_df = (
        all_df.groupby(by="product_category_name")
        .order_id.count()
        .sort_values(ascending=False)
        .reset_index()
    )
    sum_orders_df = sum_orders_df.rename(columns={"order_id": "quantity"})

    col1, col2 = st.columns(2)
    with col1:
        sort_by_product = st.selectbox(
            "Urutkan berdasarkan",
            ["Jumlah Terjual", "Nama Kategori Produk"],
            key="product_sort",
        )
    with col2:
        sort_order_product = st.radio(
            "Urutan",
            ["Dari terkecil", "Dari terbesar"],
            horizontal=True,
            key="product_order",
        )

    if sort_by_product == "Jumlah Terjual":
        sort_column_product = "quantity"
    else:
        sort_column_product = "product_category_name"

    ascending_product = True if sort_order_product == "Dari terkecil" else False
    sorted_product_df = sum_orders_df.sort_values(
        by=sort_column_product, ascending=ascending_product
    )

    fig, ax = plt.subplots(figsize=(16, 6))

    sns.barplot(
        x="quantity",
        y="product_category_name",
        data=sorted_product_df.head(10),
        palette="Greens_d",
        hue="product_category_name",
    )
    ax.set_title("Kategori Produk Berdasarkan Jumlah Terjual")
    ax.set_xlabel("Jumlah Terjual")
    ax.set_ylabel("Kategori Produk")

    st.pyplot(fig)

    # Tampilkan data frame
    st.subheader("Data Produk Yang paling banyak dan sedikit dibeli")
    with st.expander("📋 Lihat Data Lengkap"):
        st.dataframe(sum_orders_df)

with tab3:
    st.header("Distribusi Geografis Transaksi")

    transaction_counts = (
        all_df.groupby("geolocation_zip_code_prefix")
        .agg(
            total_transactions=("customer_id", "count"),
            latitude=("geolocation_lat", "first"),
            longitude=("geolocation_lng", "first"),
            city=("geolocation_city", "first"),
            state=("geolocation_state", "first"),
        )
        .reset_index()
    )

    m = folium.Map(location=[-23.5505, -46.6333], zoom_start=4)

    heat_data = [
        [row["latitude"], row["longitude"], row["total_transactions"]]
        for _, row in transaction_counts.iterrows()
    ]
    HeatMap(heat_data, radius=15, blur=20).add_to(m)

    top_10 = transaction_counts.nlargest(10, "total_transactions")
    for _, row in top_10.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["total_transactions"] / 50,
            color="blue",
            fill=True,
            fill_color="blue",
            popup=f"{row['city']} - {row['total_transactions']} transaksi",
        ).add_to(m)

    # Tampilkan peta
    st_folium(m, width=1200, height=600)
