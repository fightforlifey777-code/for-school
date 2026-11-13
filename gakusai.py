import streamlit as st

price = "price"
cost = "cost"
products = {
    "チーズスティック":{price: 500,"cost": 300},
    "さつまいもスティック":{price: 400,"cost": 200},
    "コーヒー":{price: 600,"cost": 100},
    "ココア":{price: 300,"cost": 150},
    }
st. title("学祭の売り上げ計算アプリ")
st.write("個数の入力")

st.divider()

st.subheader("個数入力")
quantities = {}

total_quantity = 0
total_sales = 0
total_cost = 0
total_profit = 0

for name, product in products.items():
    quantity = st.number_input(
        f"{name}\n (売値: {product["price"]}円, 原価: {product["cost"]}円)", 
        min_value=0,
        step=1,
        key=name
    )
    quantities[name] = quantity
    sales = quantity * product["price"]
    cost = quantity * product["cost"]
    profit = sales - cost
    total_quantity += quantity
    total_sales += sales
    total_cost += cost
    total_profit += profit

st.divider()
col1, col2 ,col3, col4 = st.columns(4)
col1.metric("合計個数","{:,}個".format(total_quantity))
col2.metric("合計売上",f"{total_sales:,.0f}円")
col3.metric("合計原価",f"{total_cost:,.0f}円")
col4.metric("合計利益",f"{total_profit:,.0f}円")

if st.button("リセット"):
    st.rerun()
