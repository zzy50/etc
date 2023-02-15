import numpy as np
import re
from typing import Optional, Tuple, List


def preprocess_filter(filename: str, filters: List[str]) -> List[bool]:
    bind = []
    for flt in filters:
        try:
            bind.append(bool(re.fullmatch(flt, filename)))
        except re.error:
            bind.append(bool(flt in filename))
    return bind

def build_filter(filename: str, filter_cond: Optional[Tuple[str, List[str]]] = None) -> bool:
    if not filter_cond:
        return True
    elif filter_cond[0] == "all":
        return all(preprocess_filter(filename, filter_cond[1]))
    elif filter_cond[0] == "any":
        return any(preprocess_filter(filename, filter_cond[1]))

def main():
    FILENAME = "123456_123456"

    ANALYSIS_DATE = [r'\d{6}', r'date_\d{6}']
    CLASSIFICATION_DATE = [r'\d{6}_\d{6}', r'classification_\d{6}_\d{6}']
    CLASS_LABEL = ["car", "bus_s", "bus_m", "truck_s", "truck_m", "truck_x"]

    DIR_FILTER = {
        "dir_include": ("any", ANALYSIS_DATE + CLASSIFICATION_DATE + CLASS_LABEL),
        "dir_exclude": ("any", ["snapshot"]),
        }
    print(FILENAME)
    print(build_filter(FILENAME, DIR_FILTER["dir_include"]))


if __name__ == "__main__":
    main()