import pandas as pd

file_path = r"E:\Codex_Projects\python_excel_learning\02_clean_sales_data\output\cleaned_sales.csv"

try:
    data = pd.read_csv(file_path)
    print("文件读取成功")
    print("数据行数：", len(data))
except FileNotFoundError:
    print("找不到文件，请检查路径")
except Exception as error:
    print("处理失败：", error)