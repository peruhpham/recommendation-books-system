import gradio as gr

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
                with gr.Column(scale=3):
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
                with gr.Column(scale=1):
                    with gr.Row():
                        del_idx = gr.Number(label="Row index to delete (start from 0)", value=0, precision=0)
                        del_btn = gr.Button("Delete Book", variant="stop")
                    with gr.Row():
                        reset_btn = gr.Button("Reset Statistics", variant="secondary")
            with gr.Row():
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
                stats_box = gr.Markdown(value=controller.get_stats(), label="📈 Statistics")

            # add_btn.click(
            #     fn=controller.add_book,
            #     inputs=[
            #         books_table, add_isbn13, add_isbn10, add_title, add_authors, add_categories,
            #         add_thumbnail, add_description, add_published_year, add_average_rating,
            #         add_num_pages, add_ratings_count, add_title_and_subtitle, add_tagged_description
            #     ],
            #     outputs=[books_table]
            # )
            # del_btn.click(
            #     fn=controller.delete_book,
            #     inputs=[books_table, del_idx],
            #     outputs=[books_table]
            # )
            # reset_btn.click(
            #     fn=controller.reset_stats,
            #     inputs=[],
            #     outputs=[]
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
    return dashboard