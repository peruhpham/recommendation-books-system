from controllers.book_controller import BookController
from views.gradio_view import create_dashboard

if __name__ == "__main__":
    controller = BookController(file_path="books_cleaned.csv")
    dashboard = create_dashboard(controller)
    dashboard.launch(debug=True)