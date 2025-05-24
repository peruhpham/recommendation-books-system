import time
import tracemalloc
from models.book_linked_list import BookLinkedList

N = 100000  # Số lượng phần tử lớn để kiểm thử

# Đo bộ nhớ sử dụng khi thêm N phần tử
tracemalloc.start()
book_list = BookLinkedList()

start = time.time()
for i in range(N):
    book_list.append(
        isbn13=str(i),
        isbn10=str(i),
        title=f"Book {i}",
        authors="Author",
        categories="Category",
        thumbnail="",
        description="Description",
        published_year="2020",
        average_rating="4.5",
        num_pages="100",
        ratings_count="50",
        title_and_subtitle="",
        tagged_description=""
    )
end = time.time()
current, peak = tracemalloc.get_traced_memory()
print(f"Thời gian thêm {N} phần tử: {end - start:.4f} giây")
print(f"Bộ nhớ đang dùng: {current / 1024 / 1024:.2f} MB; Đỉnh: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()

# Đo thời gian tìm kiếm phần tử cuối
start = time.time()
results = book_list.search("title", f"Book {N-1}")
end = time.time()
print(f"Thời gian tìm kiếm phần tử cuối: {end - start:.6f} giây")

# Đo thời gian xóa phần tử đầu
start = time.time()
book_list.delete(0)
end = time.time()
print(f"Thời gian xóa phần tử đầu: {end - start:.6f} giây")