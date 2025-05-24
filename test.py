import gradio as gr

# Hàm tìm kiếm giả lập
def search_books(query):
    sample_books = [
        ["Harry Potter and the Philosopher's Stone", "J.K. Rowling"],
        ["The Hobbit", "J.R.R. Tolkien"],
        ["The Catcher in the Rye", "J.D. Salinger"],
        ["To Kill a Mockingbird", "Harper Lee"],
    ]
    # Lọc kết quả tìm kiếm
    results = [
        [book[0], book[1]]
        for book in sample_books
        if query.lower() in book[0].lower() or query.lower() in book[1].lower()
    ]
    return results if results else [["No results found", ""]]

# Giao diện Gradio
def create_interface():
    sample_books = [
        ["Harry Potter and the Philosopher's Stone", "J.K. Rowling"],
        ["The Hobbit", "J.R.R. Tolkien"],
        ["The Catcher in the Rye", "J.D. Salinger"],
        ["To Kill a Mockingbird", "Harper Lee"],
    ]

    with gr.Blocks() as demo:
        gr.Markdown("# 📚 Real-Time Book Search with Data Table")

        with gr.Row():
            # Textbox để nhập query
            query_box = gr.Textbox(
                label="Search Books",
                placeholder="Enter book title or author"
            )
            # Bảng hiển thị dữ liệu ban đầu
            books_table = gr.Dataframe(
                value=sample_books,
                headers=["Title", "Author"],
                label="All Books",
                interactive=False
            )

        with gr.Row():
            # Bảng hiển thị kết quả tìm kiếm
            search_results = gr.Dataframe(
                value=[["", ""]],  # Dữ liệu ban đầu rỗng
                headers=["Title", "Author"],
                label="Search Results",
                interactive=False
            )

        # Gắn sự kiện khi thay đổi Textbox
        query_box.change(fn=search_books, inputs=query_box, outputs=search_results)

    return demo

# Chạy ứng dụng
demo = create_interface()
demo.launch()
