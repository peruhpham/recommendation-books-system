import csv
import gradio as gr

class BookNode:
    def __init__(self, isbn13, isbn10, title, authors, categories, thumbnail, description,
                published_year, average_rating, num_pages, ratings_count, title_and_subtitle,
                tagged_description, content):
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.title = title
        self.authors = authors
        self.categories = categories
        self.thumbnail = thumbnail
        self.description = description
        self.published_year = published_year
        self.average_rating = average_rating
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.title_and_subtitle = title_and_subtitle
        self.tagged_description = tagged_description
        self.content = content
        self.next = None

class BookLinkedList:
    def __init__(self):
        self.head = None

    def add_book(self, book_data):
        new_node = BookNode(**book_data)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def search(self, field, value):
        results = []
        cur = self.head
        idx = 1
        while cur:
            node_value = getattr(cur, field, "")
            if value.strip().lower() in str(node_value).strip().lower():
                results.append([
                    idx,
                    cur.isbn13,
                    cur.isbn10,
                    cur.title,
                    cur.authors,
                    cur.categories,
                    cur.published_year,
                    cur.average_rating
                ])
            cur = cur.next
            idx += 1
        return results

###############################################################################
def load_books_from_csv(file_path):
    book_list = BookLinkedList()
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_list.add_book(row)
    return book_list

book_list = load_books_from_csv("books_cleaned.csv")

def get_all_books():
    results = []
    cur = book_list.head
    idx = 1
    while cur:
        results.append([
            idx,
            cur.isbn13,
            cur.isbn10,
            cur.title,
            cur.authors,
            cur.categories,
            cur.published_year,
            cur.average_rating
        ])
        cur = cur.next
        idx += 1
    return results

def search_books(field, value):
    if not field or not value:
        return []
    res = book_list.search(field, value)
    return res

search_fields = ["title", "authors", "categories", "published_year", "average_rating"]

with gr.Blocks() as demo:
    gr.Markdown("# 📚 Tìm kiếm sách theo thời gian thực")

    with gr.Row():
        gr.Dataframe(
            value=get_all_books(),
            headers=["Index", "ISBN13", "ISBN10", "Title", "Authors", "Categories", "Year", "Rating"],
            interactive=False,
            label="Danh sách sách (Toàn bộ)"
        )

    with gr.Row():
        with gr.Column(scale=1):
            field_dropdown = gr.Dropdown(choices=search_fields, label="Chọn trường tìm kiếm")
            search_input = gr.Textbox(label="Nhập từ khóa tìm kiếm")
        with gr.Column(scale=2):
            search_results = gr.Dataframe(
                headers=["Index", "ISBN13", "ISBN10", "Title", "Authors", "Categories", "Year", "Rating"],
                interactive=False,
                label="Kết quả tìm kiếm"
            )

    # Gắn sự kiện .input() để khi nhập từng ký tự thì gọi hàm tìm kiếm
    search_input.input(fn=search_books, inputs=[field_dropdown, search_input], outputs=search_results)

demo.launch()
