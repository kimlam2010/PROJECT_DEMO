import logging
from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import pytz

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Kết nối cơ sở dữ liệu PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:Vn-611989@localhost/market_data"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Định nghĩa mô hình dữ liệu
class MarketData(Base):
    __tablename__ = 'market_data'
    id = Column(Integer, primary_key=True)
    data_type = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Fetch functions
QUANDL_API_KEY = "bCVm9tidn7epQobamnj7"

def fetch_oil_price():
    api_url = f"https://www.quandl.com/api/v3/datasets/CHRIS/CME_CL1.json?api_key={QUANDL_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['dataset']['data'][0][1]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching oil price: {e}")
        return None

def fetch_rice_price():
    api_url = f"https://www.quandl.com/api/v3/datasets/WORLDBANK/WLD_RICE.json?api_key={QUANDL_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['dataset']['data'][0][1]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching rice price: {e}")
        return None

def fetch_fed_rate():
    api_url = f"https://www.quandl.com/api/v3/datasets/FED/RIFSPFF_N_M.json?api_key={QUANDL_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['dataset']['data'][0][1]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching fed rate: {e}")
        return None

def fetch_inflation():
    api_url = f"https://www.quandl.com/api/v3/datasets/RATEINF/INFLATION_USA.json?api_key={QUANDL_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['dataset']['data'][0][1]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching inflation: {e}")
        return None

def fetch_bitcoin_price():
    api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()['bitcoin']['usd']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching bitcoin price: {e}")
        return None

# Lưu dữ liệu vào cơ sở dữ liệu
def save_data(data_type, value):
    session = Session()
    new_data = MarketData(data_type=data_type, value=value, timestamp=datetime.datetime.now(pytz.timezone('Asia/Bangkok')))
    session.add(new_data)
    session.commit()
    session.close()

# Thu thập dữ liệu và lưu trữ
def collect_data():
    oil_price = fetch_oil_price()
    if oil_price is not None:
        save_data('oil_price', oil_price)

    rice_price = fetch_rice_price()
    if rice_price is not None:
        save_data('rice_price', rice_price)

    fed_rate = fetch_fed_rate()
    if fed_rate is not None:
        save_data('fed_rate', fed_rate)

    inflation = fetch_inflation()
    if inflation is not None:
        save_data('inflation', inflation)

    bitcoin_price = fetch_bitcoin_price()
    if bitcoin_price is not None:
        save_data('bitcoin_price', bitcoin_price)

# Lịch trình thu thập dữ liệu
scheduler = BackgroundScheduler(timezone='Asia/Bangkok')
scheduler.add_job(collect_data, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def home():
    return jsonify({"status": "Server is running"})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
