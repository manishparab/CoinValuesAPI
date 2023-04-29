import time
from typing import Awaitable

import aiohttp
import requests
from model.asset import Asset
from model.asset_price import AssetPrice


class CoinCap:

    @staticmethod
    async def get_asset_data_historical(asset: Asset, url: str) -> Awaitable[list[AssetPrice]]:
        try:
            asset_price_history_list: list[AssetPrice] = []
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.ok:
                        response_json: dict() = await response.json()
                        asset_price_history_data_list = response_json["data"]
                        for ph in asset_price_history_data_list:
                            asset_price_history_list.append(AssetPrice(
                                float(ph["priceUsd"]),
                                int(ph["time"])/1000,
                                asset.name,
                                asset.id))
                        return asset_price_history_list
                    else:
                        raise Exception("error while fetching from {0}".format(url))
        except Exception as error:
            raise error

    @staticmethod
    async def get_asset_data(url: str) -> Awaitable[list[AssetPrice]]:
        try:
            asset_price_list: list[AssetPrice] = []
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.ok:
                        response_json: dict() = await response.json()
                        response_data = response_json["data"]
                        for record in response_data:
                            asset_price_list.append(AssetPrice(
                                float(record["priceUsd"]),
                                time.time(),
                                record["name"],
                                record["id"]))
                        return asset_price_list
                    else:
                        raise Exception("error while fetching from {0}".format(url))
        except Exception as error:
            raise error


