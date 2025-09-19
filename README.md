# Hệ thống Quản lý Bãi đỗ xe Thông minh

Đây là đồ án ngành được phát triển bởi Lý Mạnh Thắng (MSSV: 2251052112), sinh viên ngành Công nghệ thông tin, Trường Đại học Mở TP. Hồ Chí Minh. Hệ thống ứng dụng **Thị giác Máy tính** và **Điện toán Biên (Edge Computing)** để tự động hóa quy trình quản lý bãi đỗ xe.

-----

## Giới thiệu

Dự án xây dựng một hệ thống quản lý bãi đỗ xe thông minh, có khả năng tự động nhận dạng biển số xe (ALPR), quản lý xe ra vào, và cung cấp một giao diện trực quan cho người quản lý. Giải pháp được thiết kế theo mô hình Điện toán Biên, với các tác vụ AI được xử lý trực tiếp trên **Raspberry Pi 5**, giúp giảm độ trễ, tiết kiệm băng thông và tăng cường bảo mật.

-----

## Các tính năng chính

  * **Nhận dạng Biển số xe Tự động (ALPR):** Sử dụng mô hình **YOLOv8n** và **PaddleOCR** để phát hiện và nhận dạng biển số xe Việt Nam với độ chính xác cao.
  * **Quản lý Ra/Vào:** Tự động ghi nhận thời gian vào/ra của phương tiện, tính toán thời gian gửi và phí đỗ xe.
  * **Cập nhật Trạng thái Bãi đỗ:** Cung cấp thông tin về tổng số chỗ, số xe trong bãi, và số chỗ còn trống theo thời gian thực.
  * **Dashboard Giám sát:** Một giao diện web trực quan hiển thị các số liệu thống kê quan trọng (tỷ lệ lấp đầy, doanh thu, lưu lượng xe) dưới dạng biểu đồ, tự động cập nhật mỗi 30 giây.

-----

## Kiến trúc hệ thống

Hệ thống được xây dựng theo mô hình phân tán gồm 3 khối chính:

1.  **Khối Xử lý tại Biên (Edge Computing):**

      * **Thiết bị:** Raspberry Pi 5.
      * **Nhiệm vụ:** Nhận luồng video từ camera, chạy các mô hình AI (YOLOv8, PaddleOCR) để xử lý hình ảnh và gửi kết quả đã được tinh lọc về máy chủ.

2.  **Khối Máy chủ (Backend Server):**

      * **Công nghệ:** Flask.
      * **Nhiệm vụ:** Cung cấp các API để nhận dữ liệu từ Raspberry Pi 5, tương tác với cơ sở dữ liệu và cung cấp dữ liệu cho giao diện người dùng.

3.  **Khối Giao diện Người dùng (Frontend):**

      * **Công nghệ:** HTML/CSS/JavaScript, Bootstrap 5, Chart.js.
      * **Nhiệm vụ:** Hiển thị thông tin vận hành cho nhân viên (giao diện check-in) và người quản lý (dashboard).

-----

## Công nghệ sử dụng

  * **AI / Machine Learning:**
      * **Phát hiện đối tượng:** YOLOv8n (train trên dữ liệu tùy chỉnh).
      * **Nhận dạng ký tự:** PaddleOCR.
      * **Thư viện:** PyTorch, OpenCV.
  * **Backend:**
      * **Framework:** Flask.
      * **Cơ sở dữ liệu:** MySQL.
  * **Frontend:**
      * HTML5, CSS3, JavaScript.
      * **Thư viện:** Bootstrap 5, Chart.js.
  * **Phần cứng:**
      * Raspberry Pi 5 (8GB RAM).
      * Camera IP.

-----

## Kết quả thực nghiệm

  * **Hiệu năng mô hình YOLOv8n:**
      * **Precision:** 0.99
      * **Recall:** 0.98
      * **mAP50-95:** 0.925
  * **Độ chính xác hệ thống ALPR:** **88.5%** (nhận dạng đúng toàn bộ ký tự).
  * **Tốc độ xử lý trung bình (trên Raspberry Pi 5):** \~380ms / khung hình (\~2.6 FPS).

-----

## Hướng dẫn cài đặt và sử dụng

### Yêu cầu

  * Python 3.8
  * Raspberry Pi 5 (hoặc máy tính có cài đặt môi trường Python).
  * MariaDB.

### Các bước cài đặt

1.  **Clone a repository:**

    ```bash
    git clone https://github.com/thang-2251052112/Smart-Parking-ALPR.git
    cd Smart-Parking-ALPR
    ```

2.  **Tạo và kích hoạt môi trường ảo:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Thiết lập cơ sở dữ liệu:**

      * Tạo một database mới trong MySQL.
      * Cấu hình thông tin kết nối trong file `config.py`.

5.  **Chạy ứng dụng:**

    ```bash
    cd backend_API/
    python run.py
    cd frontend
    python run.py
    ```

    Mở trình duyệt và truy cập vào `http://127.0.0.1:5000`.

-----
