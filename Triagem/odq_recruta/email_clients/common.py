"""
Tipos e helpers comuns para paginação/download
"""
from typing import Any, Dict, List

def paginate(items: List[Any], page_size: int):
    for i in range(0, len(items), page_size):
        yield items[i:i+page_size]

