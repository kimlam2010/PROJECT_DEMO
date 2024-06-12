import nasdaqdatalink
import pandas as pd
import matplotlib.pyplot as plt

# Thiết lập API key cho Nasdaq Data Link
nasdaqdatalink.ApiConfig.api_key = "bCVm9tidn7epQobamnj7"

# Lấy dữ liệu giá dầu (dùng mã OPEC/ORB là ví dụ)
data = nasdaqdatalink.get('OPEC/ORB', start_date='2022-01-01')

# Đặt lại tên cột để dễ sử dụng
data.columns = ['Price']

# Hiển thị dữ liệu
print(data)

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Price'], label='Oil Price')
plt.title('Oil Price Daily from 2022 to Now')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()
