import pandas as pd

file_path = r"E:\Codex_Projects\python_excel_learning\02_clean_sales_data\output\cleaned_sales.csv"
output_file = r"E:\Codex_Projects\python_excel_learning\02_clean_sales_data\output\product_summary.xlsx"

data = pd.read_csv(file_path)

summary = data.groupby("产品").agg(
    总数量=("数量", "sum"),
    总金额=("金额", "sum"),
).reset_index()

summary.to_excel(output_file, index=False)

print("汇总报表已保存：")
print(output_file)