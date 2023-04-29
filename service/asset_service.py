import asyncio
from configparser import ConfigParser
from model.asset import Asset
from model.asset_price import AssetPrice
from model.asset_price_history import AssetPriceHistory
from repository.coincap import CoinCap
from repository.asset_price_repository import AssetPriceRepository


class AssetService:

    def __init__(self, config: ConfigParser):
        self.base_url = config['coincap']['base_url']

    async def load_asset_data_history(self):
        total_records: int = await AssetPriceRepository.get_asset_prices_record_count()
        if total_records == 0:
            assets: list[Asset] = await AssetPriceRepository.get_assets()
            if len(assets) == 0:
                raise Exception("assets data not preloaded")
            asset_price_list: list[AssetPrice] = []
            for asset in assets:
                url: str = "{0}/v2/assets/{1}/history?interval=m1".format(self.base_url, asset.id)
                asset_price: list[AssetPrice]= await CoinCap.get_asset_data_historical(asset, url)
                asset_price_list += asset_price

            await AssetPriceRepository.insert_assets_prices(asset_price_list)

    def load_current_asset_data(self):
        asyncio.run(self.load_current_asset_data_async())

    async def load_current_asset_data_async(self):
        print("loading current asset prices..")
        assets: list[Asset] = await AssetPriceRepository.get_assets()
        asset_ids: str = ",".join([asset.id for asset in assets])
        url: str = "{0}/v2/assets?ids={1}".format(self.base_url, asset_ids)
        asset_price_list: list[AssetPrice] = await CoinCap.get_asset_data(url)
        await AssetPriceRepository.insert_assets_prices(asset_price_list)

    @staticmethod
    async def get_interval_prices_for_asset(asset_id: str) -> AssetPriceHistory:
        asset: Asset = await AssetPriceRepository.get_asset_by_id(asset_id)
        price_latest, price_one_hour_ago, price_four_hour_ago, price_eight_hour_ago, price_twenty_four_hour_ago = \
            await asyncio.gather(AssetPriceRepository.get_assets_price_for_interval(asset_id, None),
                                 AssetPriceRepository.get_assets_price_for_interval(asset_id, 1),
                                 AssetPriceRepository.get_assets_price_for_interval(asset_id, 4),
                                 AssetPriceRepository.get_assets_price_for_interval(asset_id, 8),
                                 AssetPriceRepository.get_assets_price_for_interval(asset_id, 24))
        return AssetPriceHistory(asset.id,
                                 asset.name,
                                 price_latest,
                                 price_one_hour_ago,
                                 price_four_hour_ago,
                                 price_eight_hour_ago,
                                 price_twenty_four_hour_ago)
