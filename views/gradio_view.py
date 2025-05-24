import gradio as gr
from controllers.book_controller import BookController


# Cập nhật mô tả khi chọn trường
def update_field_desc(field):
    descs = {
        "title": "**Tiêu đề sách:** Tìm kiếm theo tên sách.",
        "authors": "**Tác giả:** Tìm kiếm theo tên tác giả.",
        "categories": "**Thể loại:** Tìm kiếm theo thể loại sách.",
        "isbn13": "**ISBN13:** Tìm kiếm theo mã ISBN13.",
        "isbn10": "**ISBN10:** Tìm kiếm theo mã ISBN10.",
        "published_year": "**Năm xuất bản:** Tìm kiếm theo năm xuất bản.",
        "average_rating": "**Đánh giá trung bình:** Tìm kiếm theo điểm đánh giá.",
        "num_pages": "**Số trang:** Tìm kiếm theo số trang.",
        "ratings_count": "**Số lượt đánh giá:** Tìm kiếm theo số lượt đánh giá.",
        "title_and_subtitle": "**Tiêu đề & phụ đề:** Tìm kiếm theo tiêu đề và phụ đề.",
        "tagged_description": "**Mô tả đã gắn thẻ:** Tìm kiếm theo mô tả đã gắn thẻ.",
    }
    return descs.get(field, "")

def create_dashboard(controller):
    with gr.Blocks(theme=gr.themes.Glass(), fill_height=True) as dashboard:
        gr.Markdown("# 📚 System Book Recommendation")

        with gr.Tab("🔍 Recommend Books"):
            with gr.Row():
                user_query = gr.Textbox(label="🔎 Enter a description of a book", placeholder="e.g., A story about forgiveness")
                submit_button = gr.Button("Find Recommendations", variant="primary")
            gr.Markdown("## Recommendations")
            with gr.Row():
                output = gr.Gallery(label="Recommended Books", columns=8, rows=2)
            with gr.Row():
                table = gr.Dataframe(
                    headers=["Index", "Title", "Authors", "Category", "Description", "Thumbnail"],
                    wrap=True,
                    interactive=True
                )
            submit_button.click(
                fn=controller.recommend_books,
                inputs=[user_query],
                outputs=[output, table]
            )

        with gr.Tab("🛠️ Book Management & Statistics"):
            with gr.Row():
                gr.Markdown("### 📚 Manage Your Books")
            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        add_isbn13 = gr.Textbox(label="ISBN13")
                        add_isbn10 = gr.Textbox(label="ISBN10")
                        add_authors = gr.Textbox(label="Authors")
                    with gr.Row():
                        add_title = gr.Textbox(label="Title")
                    with gr.Row():
                        add_categories = gr.Textbox(label="Categories")
                        add_thumbnail = gr.Textbox(label="Thumbnail URL")
                    with gr.Row():
                        add_description = gr.Textbox(label="Description")
                    with gr.Row():
                        add_published_year = gr.Textbox(label="Published Year")
                        add_average_rating = gr.Textbox(label="Average Rating")
                        add_num_pages = gr.Textbox(label="Num Pages")
                    with gr.Row():
                        add_ratings_count = gr.Textbox(label="Ratings Count")
                        add_title_and_subtitle = gr.Textbox(label="Title and Subtitle")
                        add_tagged_description = gr.Textbox(label="Tagged Description")
                    add_btn = gr.Button("Add Book", variant="primary")
                with gr.Column(scale=5):
                    gr.Markdown("## 📊 Books Table")
                    with gr.Row():
                        books_table = gr.Dataframe(
                            value=controller.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"]),
                            headers=["Index", "Title", "Authors", "Description", "Thumbnail"],
                            wrap=True,
                            interactive=True,
                            label="Books Table"
                        )
                    with gr.Row():
                        with gr.Column(scale=3):
                            del_idx = gr.Number(label="Row index to delete (start from 0)", value=0, precision=0)
                            del_btn = gr.Button("Delete Book", variant="stop")
                            with gr.Row():
                                reset_btn = gr.Button("Reset Statistics", variant="secondary")
                        with gr.Column(scale=2):
                            stats_box = gr.Markdown(value=controller.get_stats(), label="📈 Statistics")

            with gr.Row():
                gr.Markdown("---") 
            with gr.Row():
                gr.Markdown("---") 
            with gr.Row():
                gr.Markdown("# 📚 Manage Search Your Books")
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        gr.Markdown("#### 🔎 Tìm kiếm sách theo trường thông tin")
                    
                    # --- Thêm vùng tìm kiếm ---
                #     with gr.Row():
                #         search_field = gr.Dropdown(
                #             choices=[
                #                 ("title", "Tiêu đề sách"),
                #                 ("authors", "Tác giả"),
                #                 ("categories", "Thể loại"),
                #                 ("isbn13", "ISBN13"),
                #                 ("isbn10", "ISBN10"),
                #                 ("published_year", "Năm xuất bản"),
                #                 ("average_rating", "Đánh giá trung bình"),
                #                 ("num_pages", "Số trang"),
                #                 ("ratings_count", "Số lượt đánh giá"),
                #                 ("title_and_subtitle", "Tiêu đề & phụ đề"),
                #                 ("tagged_description", "Mô tả đã gắn thẻ"),
                #             ],
                #             label="Chọn trường thông tin",
                #             value="title"
                #         )

                #         field_desc = gr.Markdown("**Tiêu đề sách:** Tìm kiếm theo tên sách.")
                #         search_value = gr.Textbox(label="Nhập giá trị cần tìm")
                #         search_btn = gr.Button("Tìm kiếm", variant="secondary")
                # with gr.Column(scale=4):
                #     with gr.Row():
                #         gr.Markdown("## 📊 Search Books Table")
                #     with gr.Row():
                #         books_table = gr.Dataframe(
                #             value=controller.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"]),
                #             headers=["Index", "Title", "Authors", "Description", "Thumbnail"],
                #             # wrap=True,
                #             interactive=True,
                #             label="Books Table"
                #         )
            with gr.Row():
                with gr.Column(scale=1):
                    search_fields = ["title", "authors", "categories", "published_year", "average_rating"]
                    field_dropdown = gr.Dropdown(choices=search_fields, label="Chọn trường tìm kiếm")
                    search_input = gr.Textbox(label="Nhập từ khóa tìm kiếm")
                with gr.Column(scale=4):
                    search_results = gr.Dataframe(
                        headers=["Index", "ISBN13", "ISBN10", "Title", "Authors", "Categories", "Year", "Rating"],
                        interactive=False,
                        wrap=True,
                        label="Kết quả tìm kiếm"
                    )
            # controller = BookController("books_cleaned.csv")
            # Gắn sự kiện .input() để khi nhập từng ký tự thì gọi hàm tìm kiếm
            search_input.input(fn=controller.search_books, inputs=[field_dropdown, search_input], outputs=search_results)

            # search_field.change(
            #     fn=update_field_desc,
            #     inputs=[search_field],
            #     outputs=[field_desc]
            # )
            
            add_btn.click(
                fn=controller.add_book,
                inputs=[books_table, add_isbn13, add_isbn10, add_title, add_authors, add_categories,
                        add_thumbnail, add_description, add_published_year, add_average_rating,
                        add_num_pages, add_ratings_count, add_title_and_subtitle, add_tagged_description],
                outputs=[books_table, stats_box]
            )
            del_btn.click(
                fn=controller.delete_book,
                inputs=[books_table, del_idx],
                outputs=[books_table, stats_box]
            )
            reset_btn.click(
                fn=controller.reset_stats,
                inputs=[],
                outputs=[stats_box]
            )
            # # Sự kiện tìm kiếm
            # search_value.input(
            #     fn=lambda field, value: controller.search_books_by_field(field, value),
            #     inputs=[search_field, search_value],
            #     outputs=[books_table]
            # )
            # search_btn.click(
            #     fn=lambda field, value: controller.search_books_by_field(field, value),
            #     inputs=[search_field, search_value],
            #     outputs=[books_table]
            # )
    return dashboard