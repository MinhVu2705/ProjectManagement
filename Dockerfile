# Sử dụng Python chính thức
FROM python:3.9-slim

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép tệp yêu cầu vào container
COPY requirements.txt requirements.txt

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

# Thiết lập biến môi trường
ENV FLASK_APP=manage.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port
EXPOSE 5000

# Lệnh chạy ứng dụng
CMD ["flask", "run"]
