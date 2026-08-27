"""检查清洗程序生成的结果是否符合基本要求。"""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "output" / "cleaned_sales.csv"
REQUIRED_COLUMNS = {"日期", "销售员", "产品", "数量", "金额"}


def main() -> None:
    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(f"找不到输出文件：{OUTPUT_FILE}")

    data = pd.read_csv(OUTPUT_FILE, encoding="utf-8-sig")
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"输出文件缺少字段：{', '.join(sorted(missing_columns))}")
    if data.empty:
        raise ValueError("输出文件没有数据行")
    if (data["数量"] <= 0).any():
        raise ValueError("输出文件中存在无效数量")
    if (data["金额"] <= 0).any():
        raise ValueError("输出文件中存在无效金额")

    print(f"结果检查通过，共 {len(data)} 行")


if __name__ == "__main__":
    main()
