from flask import Flask, jsonify
from flask_cors import CORS
from configparser import ConfigParser
from apscheduler.schedulers.background import BackgroundScheduler
from service.asset_service import AssetService
import asyncio

# create flask application
app = Flask(__name__)
# allow cors
CORS(app)

# read configuration file
file = 'config.ini'
config = ConfigParser()
config.read(file)


# flask application api route to get prices for asset
@app.route('/asset/<asset_id>/prices')
async def prices(asset_id: str):
    try:
        return jsonify(await AssetService.get_interval_prices_for_asset(asset_id))
    except Exception as error:
        return "error occurred while getting prices, details {0} ".format(str(error)), 500


async def main():
    try:
        asset_service = AssetService(config)
        # used for initial load of data,
        # if price data is empty we load the data from API and push to db
        await asset_service.load_asset_data_history()

        # creating schedular job which runs every 60 seconds to get the live data from API and save to DB
        # A scheduler runs in the background using a separate thread
        # https://apscheduler.readthedocs.io/en/3.x/modules/schedulers/background.html
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(asset_service.load_current_asset_data, 'interval', seconds=int(config['schedular']['interval']))
        scheduler.start()
    except Exception as error:
        print("error occurred, please fix the error and rerun the application : " + str(error))


asyncio.run(main())

if __name__ == '__main__':
    app.run()
