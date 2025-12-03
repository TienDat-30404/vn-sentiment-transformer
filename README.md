I. Đề tài và chức năng chính
1. Chủ đề
Dự án Xây dựng Trợ lý Phân loại Cảm xúc Tiếng Việt tập trung vào việc xử lý ngôn ngữ tự nhiên (NLP) cho Tiếng Việt, sử dụng mô hình Transformer để phân tích và phân loại cảm xúc từ văn bản đầu vào.

2. Chức năng Cốt lõi
+ Phân loại Cảm xúc: Phân tích câu Tiếng Việt và đưa ra nhãn cảm xúc là POSITIVE (Tích cực), NEGATIVE (Tiêu cực), hoặc NEUTRAL (Trung tính).
+ Xử lý ngôn ngữ: Tự động chuẩn hóa văn bản Tiếng Việt, bao gồm việc thêm dấu và chuẩn hóa từ ngữ (nlp_processor.py).
+ Lưu trữ Dữ liệu An toàn: Sử dụng cơ sở dữ liệu SQLite để lưu trữ lịch sử phân loại. Việc ghi dữ liệu sử dụng Parameterized Queries để ngăn chặn các cuộc tấn công SQL Injection (database.py).
+ Giao diện Trực quan: Ứng dụng web được xây dựng bằng Streamlit, cung cấp giao diện nhập liệu, hiển thị kết quả và biểu đồ thống kê cảm xúc.

II. Cấu trúc Source Code
Mã nguồn được tổ chức thành các file chính, mỗi file đảm nhiệm một chức năng cụ thể:

File Name                   Chức năng
main.py                     Khởi chạy ứng dụng web Streamlit, quản lý giao diện, và tải mô hình Transformer.
nlp_processor.py            Chứa logic tiền xử lý văn bản và logic gọi mô hình Transformer để phân loại.
database.py                 Quản lý kết nối và thao tác với cơ sở dữ liệu SQLite, bao gồm hàm lưu trữ an toàn.
requirements.txt            Danh sách tất cả các thư viện Python cần thiết cho dự án.

III. Yêu cầu và Hướng dẫn Chạy
1. Yêu cầu Môi trường
    + Python: Phiên bản 3.8 trở lên.
    + Git: Đã được cài đặt.
2. Hướng dẫn Cài đặt
    - Clone Repository: Tải mã nguồn về máy tính.
        + Clone Repository: git clone git@github.com:TienDat-30404/vn-sentiment-transformer.git
        + cd vn-sentiment-transformer
    - Cài đặt Thư viện: Cài đặt tất cả các thư viện cần thiết
        + pip install -r requirements.txt
3. Cách chạy ứng dụng: 
Khởi chạy ứng dụng web bằng lệnh Streamlit: streamlit run main.py

* Lưu ý : Ứng dụng sẽ tự động mở trong trình duyệt web : http://localhost:8501. Lần đầu chạy, mô hình Transformer sẽ được tải về, quá trình này có thể mất vài phút.