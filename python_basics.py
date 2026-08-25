import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def show_summary(data):
    print("数据行数：", len(data))
    print("总数量：", data["数量"].sum())
    print("总金额：", data["金额"].sum())


file_path = r"E:\Codex_Projects\python_excel_learning\02_clean_sales_data\output\cleaned_sales.csv"

try:
    sales_data = load_data(file_path)
    show_summary(sales_data)
except Exception as error:
    print("处理失败：", error)