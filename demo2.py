import nasdaqdatalink
import pandas as pd
import matplotlib.pyplot as plt
import time

# Thiết lập API key cho Nasdaq Data Link
nasdaqdatalink.ApiConfig.api_key = "bCVm9tidn7epQobamnj7"

# Hàm lấy dữ liệu và đặt tên cột với delay
def get_data(dataset_code, column_name):
    data = nasdaqdatalink.get(dataset_code, start_date='2022-01-01')
    data.columns = [column_name]
    time.sleep(1)  # Delay 1 giây giữa mỗi lần gọi API
    return data

try:
    # Lấy dữ liệu giá dầu WTI
    oil_data = get_data('FRED/DCOILWTICO', 'Oil Price')
    
    # Lấy dữ liệu lãi suất của Fed
    fed_funds_data = get_data('FRED/FEDFUNDS', 'Fed Funds Rate')

    # In toàn bộ bản giá trị của cả hai bộ dữ liệu
    print("Oil Data:")
    print(oil_data)
    print("\nFed Funds Data:")
    print(fed_funds_data)

    # Kết hợp hai bộ dữ liệu dựa trên ngày
    combined_data = pd.merge(oil_data, fed_funds_data, left_index=True, right_index=True)

    # Vẽ biểu đồ với hai trục y
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Trục y cho giá dầu
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Oil Price (USD)', color='tab:blue')
    ax1.plot(combined_data.index, combined_data['Oil Price'], label='Oil Price', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Trục y cho lãi suất của Fed
    ax2 = ax1.twinx()
    ax2.set_ylabel('Fed Funds Rate (%)', color='tab:orange')
    ax2.plot(combined_data.index, combined_data['Fed Funds Rate'], label='Fed Funds Rate', color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Thêm tiêu đề và lưới
    plt.title('Oil Price and Fed Funds Rate from 2022 to Now')
    fig.tight_layout()
    plt.grid(True)

    # Hiển thị biểu đồ
    plt.show()

except nasdaqdatalink.errors.data_link_error.NotFoundError as e:
    print(f"Dataset not found: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
