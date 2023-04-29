from dataclasses import dataclass


@dataclass
class AssetPriceHistory:
    asset_id: str
    asset_name: str
    price_latest: float
    price_one_hour_ago: float
    price_four_hour_ago: float
    price_eight_hour_ago: float
    price_twenty_four_hour_ago: float
