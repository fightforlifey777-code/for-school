import streamlit as st
import pandas as pd
from io import BytesIO

if "date_list" not in st.session_state:
    st.session_state.date_list = []

with st.form("product_form"):
     product_name = st.selectbox("商品名",["チーズスティック","さつまいもスティック","コーヒー","ココア"])
     quantity = st.number_input("個数",min_value=1,value=1)
     submit_button = st.form_submit_button("完了")


price = "price"
cost = "cost"
products = {
    "チーズスティック":{price: 500,"cost": 300},
    "さつまいもスティック":{price: 400,"cost": 200},
    "コーヒー":{price: 600,"cost": 100},
    "ココア":{price: 300,"cost": 150},
    }
st.title("学祭の売り上げ計算アプリ")
st.write("個数の入力")

if "history"not in st.session_state:
    st.session_state.history = {name: 0 for name in products}


with st.form("sales_form", clear_on_submit=True):
    st.subheader("商品ごとの個数入力")
    current_input = {}

    for name, product in products.items():
        
                quantity = st.number_input(
                    f"{name}\n (売値:{product["price"]}円、原価: {product["cost"]}円)", 
                    min_value=0,
                    value=0,
                    step=1,
                    key=name
        )
                current_input[name] = quantity
    submit_button = st.form_submit_button("完了")
    
if submit_button:
    for name, quantity in current_input.items():
        st.session_state.history[name] += quantity
    st.success("入力が完了しました。")

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

excel_details = []

for d in details:
    excel_details.append({
        "商品名": d["name"],
        "個数": d["quantity"],
        "売上": d["sales"],
        "原価": d["cost"],
        "利益": d["profit"]
    })
for d in details:
    st.markdown(f"**{d['name']}**")
    st.write(f"個数: {d['quantity']}個")
    st.write(f"売上: {d['sales']:,.0f}円")
    st.write(f"原価: {d['cost']:,.0f}円")
    st.write(f"利益: {d['profit']:,.0f}円")
    st.markdown("---")

    df = pd.DataFrame(excel_details)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="売上詳細")
    excel_data = output.getvalue()

    st.download_button(
        label="Excelでダウンロード",
        data=excel_data,
        file_name="売上詳細.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if st.button("リセット"):
    st.session_state.history = {name: 0 for name in products}
    st.rerun()
