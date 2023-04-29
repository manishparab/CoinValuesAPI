from dataclasses import dataclass


@dataclass
class AssetPrice:
    priceUsd: float
    time: int
    name: str
    id: str
