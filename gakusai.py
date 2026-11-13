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

if "history"not in st.session_state:
    st.session_state.history = {name: 0 for name in products}


with st.form("input_form"):
    st.subheader("商品ごとの個数入力")
    current_input = {}

for name, product in products.items():
    quantity = st.number_input(
        f"{name}\n (売値: {product["price"]}円, 原価: {product["cost"]}円)", 
        min_value=0,
        value=0,
        step=1,
        key=f"input_{name}"
    )
    current_input[name] = quantity

submit_button = st.button("完了")

if submit_button:
    for name, quantity in current_input.items():
        st.session_state.history[name] += quantity
    st.success("入力が完了しました。")

    for name in products:
        st.session_state[name] = 0

    st.rerun()

st.divider()

total_quantity = 0
total_sales = 0
total_cost = 0
total_profit = 0


details = []
for name, product in products.items():
    quantity = st.session_state.history.get(name, 0)
    sales = quantity * product["price"]
    cost = quantity * product["cost"]
    profit = sales - cost
    total_quantity += quantity
    total_sales += sales
    total_cost += cost
    total_profit += profit

    details.append({
        "name":name,
        "quantity":quantity,
        "sales":sales,
        "cost":cost,
        "profit":profit
})

st.divider()
st.subheader("売上詳細")
col1, col2 ,col3, col4 = st.columns(4)
col1.metric("合計個数","{:,}個".format(total_quantity))
col2.metric("合計売上",f"{total_sales:,.0f}円")
col3.metric("合計原価",f"{total_cost:,.0f}円")
col4.metric("合計利益",f"{total_profit:,.0f}円")

for d in details:
    st.markdown(f"**{d['name']}**")
    st.write(f"個数: {d['quantity']}個")
    st.write(f"売上: {d['sales']:,.0f}円")
    st.write(f"原価: {d['cost']:,.0f}円")
    st.write(f"利益: {d['profit']:,.0f}円")
    st.markdown("---")

if st.button("リセット"):
    st.session_state.history = {name: 0 for name in products}
    st.rerun()
