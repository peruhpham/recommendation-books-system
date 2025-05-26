# Hệ Thống Gợi Ý Sách (Book Recommender LLM)

## 1. Mô tả dự án

Hệ thống Gợi Ý Sách sử dụng mô hình học sâu (Deep Learning) và ngôn ngữ tự nhiên (NLP) để phân tích, gợi ý sách dựa trên nội dung mô tả hoặc danh mục sách. Ứng dụng bao gồm các chức năng:

* Tìm kiếm và gợi ý sách dựa trên mô tả người dùng.
* Quản lý danh sách sách (thêm, xóa) và thống kê dữ liệu.

Dự án được xây dựng sử dụng thư viện [Gradio](https://gradio.app/) để tạo giao diện người dùng thân thiện.

---

## 2. Yêu cầu hệ thống

* **Ngôn ngữ lập trình**: Python 3.8+
* **Thư viện cần thiết**: Xem chi tiết trong file `requirements.txt`
* **Các công cụ**: Virtual Environment (khuyến nghị), IDE hỗ trợ Python như PyCharm, VSCode.

---

## 3. Cấu trúc thư mục

```plaintext
recommendation-books-system/
│
├── models/
│   ├── book_node.py             # Định nghĩa cấu trúc dữ liệu sách
│   ├── book_linked_list.py      # Triển khai danh sách liên kết đơn để quản lý sách
│   └── __init__.py
│
├── controllers/
│   ├── book_controller.py       # Xử lý logic nghiệp vụ liên quan đến sách
│   └── __init__.py
│
├── views/
│   ├── gradio_view.py           # Giao diện người dùng với Gradio
│   └── __init__.py
│
├── utils/
│   ├── translation.py           # Công cụ hỗ trợ dịch ngôn ngữ
│   └── __init__.py
│
├── main.py                       # Điểm khởi động của ứng dụng
├── books_cleaned.csv             # Dữ liệu sách đầu vào
└── requirements.txt              # Danh sách các thư viện cần thiết
```

---

## 4. Hướng dẫn cài đặt và sử dụng

### Bước 1: Sao chép dự án

```bash
git clone https://github.com/peruhpham/recommendation-books-system.git
cd recommendation-books-system
```

### Bước 2: Tạo môi trường ảo và cài đặt thư viện

```bash
python -m venv venv
source venv/bin/activate      # Đối với Linux/macOS
venv\Scripts\activate        # Đối với Windows
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng

```bash
python main.py
```

Truy cập giao diện tại [http://localhost:7860](http://localhost:7860).

---

## 5. Các tính năng chính

### 5.1. Gợi ý sách

* Người dùng nhập nội dung mô tả (ví dụ: "Một câu chuyện về tình yêu và sự tha thứ")
* Hệ thống sẽ hiển thị danh sách sách gợi ý kèm hình ảnh và thông tin chi tiết.

### 5.2. Quản lý sách

* **Thêm sách mới**: Nhập thông tin ISBN, tiêu đề, tác giả, năm xuất bản, v.v.
* **Xóa sách**: Chọn hàng cần xóa dựa trên chỉ số.
* **Tìm kiếm sách**: Chọn trường dữ liệu: title, author, v.v ... để tìm kiếm linh hoạt với bất kì đầu vào.
* **Đo thời gian**: Quan sát thời gian thực hiện của một số tiến trình, các hàm, các model, v.v... .
* **File chương trình đo thời gian**: run python benchmark.py

### 5.3. Thống kê

* Hiển thị số lượng sách đã thêm, đã xóa.

---

## 6. Ghi chú

* **Dữ liệu mẫu**: File `books_cleaned.csv` chứa dữ liệu sách mẫu.
* **Mở rộng**: Có thể tích hợp thêm các API gợi ý sách từ bên thứ ba hoặc cải tiến giao diện người dùng.

---

## 7. Đóng góp

Mọi đóng góp và phản hồi xin vui lòng gửi về qua email hoặc tạo một Pull Request trên GitHub.

---

## 8. Tác giả

**Tên nhóm/Người phát triển**: \<Nhóm 08>
**Email**: \<n22dccn160@student.ptithcm.edu.vn>
