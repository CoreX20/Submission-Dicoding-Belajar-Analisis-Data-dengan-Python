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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            f"{sum_order_payments_df.iloc[0]['payment_type']}",
            value=sum_order_payments_df.iloc[0]["quantity"],
        )
    with col2:
        st.metric(
            f"{sum_order_payments_df.iloc[1]['payment_type']}",
            value=sum_order_payments_df.iloc[1]["quantity"],
        )
    with col3:
        st.metric(
            f"{sum_order_payments_df.iloc[2]['payment_type']}",
            value=sum_order_payments_df.iloc[2]["quantity"],
        )
    with col4:
        st.metric(
            f"{sum_order_payments_df.iloc[3]['payment_type']}",
            value=sum_order_payments_df.iloc[3]["quantity"],
        )

    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    sns.barplot(
        x="payment_type",
        y="quantity",
        data=sum_order_payments_df.head(5),
        ax=ax[0],
        palette="Blues_d",
        hue="payment_type",
    )
    ax[0].set_title("Metode Pembayaran Paling Sering Digunakan")
    ax[0].set_ylabel("Jumlah Transaksi")
    ax[0].set_xlabel("Metode Pembayaran")

    sns.barplot(
        x="payment_type",
        y="quantity",
        data=sum_order_payments_df.sort_values(by="quantity", ascending=True),
        ax=ax[1],
        palette="Reds_d",
        hue="payment_type",
    )
    ax[1].set_title("Metode Pembayaran Paling Jarang Digunakan")
    ax[1].set_ylabel("Jumlah Transaksi")
    ax[1].set_xlabel("Metode Pembayaran")

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

    fig, ax = plt.subplots(1, 2, figsize=(16, 6))

    sns.barplot(
        x="quantity",
        y="product_category_name",
        data=sum_orders_df.head(10),
        ax=ax[0],
        palette="Greens_d",
        hue="product_category_name",
    )
    ax[0].set_title("Kategori produk yang paling banyak Dibeli")
    ax[0].set_xlabel("Jumlah Terjual")
    ax[0].set_ylabel("Kategori Produk")

    sns.barplot(
        x="quantity",
        y="product_category_name",
        data=sum_orders_df.sort_values(by="quantity", ascending=True).head(10),
        ax=ax[1],
        palette="Oranges_d",
        hue="product_category_name",
    )
    ax[1].invert_xaxis()
    ax[1].set_title("Kategori produk yang paling sedikit Dibeli")
    ax[1].set_xlabel("Jumlah Terjual")
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].tick_params(axis="y", labelsize=15)
    ax[1].set_ylabel("")

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
