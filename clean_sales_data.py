# -*- coding: utf-8 -*-
"""清洗销售 CSV 数据。"""

from pathlib import Path
import logging

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input" / "raw_sales.csv"
OUTPUT_FILE = BASE_DIR / "output" / "cleaned_sales.csv"
LOG_FILE = BASE_DIR / "logs" / "clean.log"


def setup_logging() -> None:
    LOG_FILE.parent.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def read_csv() -> pd.DataFrame:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return pd.read_csv(INPUT_FILE, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("无法识别 CSV 文件编码")


def main() -> None:
    setup_logging()
    data = read_csv()
    logging.info("原始数据：%d 行", len(data))

    data.columns = [str(column).strip() for column in data.columns]
    required = {"日期", "销售员", "产品", "数量", "金额"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"缺少列：{', '.join(sorted(missing))}")

    data["日期"] = pd.to_datetime(data["日期"], errors="coerce")
    data["数量"] = pd.to_numeric(data["数量"], errors="coerce")
    data["金额"] = pd.to_numeric(data["金额"], errors="coerce")

    before = len(data)
    data = data.drop_duplicates(subset=["日期", "销售员", "产品", "数量", "金额"])
    logging.info("删除重复行：%d 行", before - len(data))

    before = len(data)
    data = data.dropna(subset=["日期", "销售员", "产品", "数量", "金额"])
    data = data[(data["数量"] > 0) & (data["金额"] > 0)]
    logging.info("删除错误行：%d 行", before - len(data))

    data["日期"] = data["日期"].dt.strftime("%Y-%m-%d")
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    logging.info("清洗完成：%s，共 %d 行", OUTPUT_FILE, len(data))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logging.exception("处理失败：%s", error)
        raise
