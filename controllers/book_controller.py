import pandas as pd
from models.book_linked_list import BookLinkedList
from utils.translation import translate_vi_to_en, translate_en_to_vi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

class BookController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.books_ll = BookLinkedList()
        self.added_count = 0
        self.deleted_count = 0
        self.load_books()
        self.embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.build_vector_db()

    def load_books(self):
        df = pd.read_csv(self.file_path, encoding='utf-8', sep=',')
        for _, row in df.iterrows():
            thumb = row.get("thumbnail", "")
            if not isinstance(thumb, str) or not thumb.startswith("http"):
                thumb = "https://via.placeholder.com/150?text=No+Image"
            self.books_ll.append(
                row.get("isbn13", ""),
                row.get("isbn10", ""),
                row.get("title", ""),
                row.get("authors", ""),
                row.get("categories", ""),
                thumb,
                row.get("description", ""),
                row.get("published_year", ""),
                row.get("average_rating", ""),
                row.get("num_pages", ""),
                row.get("ratings_count", ""),
                row.get("title_and_subtitle", ""),
                row.get("tagged_description", "")
            )

    def build_vector_db(self):
        documents = [Document(page_content=f"{node.title} - {node.description}") for node in self.books_ll.iter_nodes()]
        self.db_books = Chroma.from_documents(documents, embedding=self.embedding_model)

    def save_books_to_csv(self):
        data = []
        for node in self.books_ll.iter_nodes():
            data.append({
                "isbn13": node.isbn13,
                "isbn10": node.isbn10,
                "title": node.title,
                "authors": node.authors,
                "categories": node.categories,
                "thumbnail": node.thumbnail,
                "description": node.description,
                "published_year": node.published_year,
                "average_rating": node.average_rating,
                "num_pages": node.num_pages,
                "ratings_count": node.ratings_count,
                "title_and_subtitle": node.title_and_subtitle,
                "tagged_description": node.tagged_description,
                "content": f"{node.title} - {node.description}"
            })
        pd.DataFrame(data).to_csv(self.file_path, index=False, encoding='utf-8')

    # def add_book(self, *args):
    #     (table, isbn13, isbn10, title, authors, categories, thumbnail, description,
    #     published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description) = args
    #     title_en = translate_vi_to_en(title)
    #     description_en = translate_vi_to_en(description)
    #     self.books_ll.append(
    #         isbn13, isbn10, title_en, authors, categories, thumbnail, description_en,
    #         published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description
    #     )
    #     self.added_count += 1
    #     content = f"{title_en} - {description_en}"
    #     self.db_books.add_documents([Document(page_content=content)])
    #     self.save_books_to_csv()
    #     return self.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"]), self.get_stats()

    def add_book(self, *args):
        (table, isbn13, isbn10, title, authors, categories, thumbnail, description,
        published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description) = args
        title_en = translate_vi_to_en(title)
        description_en = translate_vi_to_en(description)
        self.books_ll.append(
            isbn13, isbn10, title_en, authors, categories, thumbnail, description_en,
            published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description
        )
        self.added_count += 1
        content = f"{title_en} - {description_en}"
        self.db_books.add_documents([Document(page_content=content)])
        self.save_books_to_csv()
        return self.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"]), self.get_stats()

    def delete_book(self, table, row_idx):
        self.books_ll.delete(int(row_idx))
        self.deleted_count += 1
        self.save_books_to_csv()
        return self.show_books_table(), self.get_stats()

    def reset_stats(self):
        self.added_count = 0
        self.deleted_count = 0
        return self.get_stats()

    def get_stats(self):
        return (
            f"**Tổng số sách:** {len(self.books_ll)}  \n"
            f"**Sách mới thêm:** {self.added_count}  \n"
            f"**Sách đã xóa:** {self.deleted_count}"
        )

    def show_books_table(self, columns=None):
        all_books = self.books_ll.to_list()
        if not all_books:
            return []
        if columns:
            return [[book.get(col, "") for col in columns] for book in all_books]
        return [[book.get(col, "") for col in all_books[0].keys()] for book in all_books]

    def recommend_books(self, query):
        translated_query = translate_vi_to_en(query)
        recs = self.db_books.similarity_search(translated_query, k=50)
        titles = [rec.page_content.split(" - ")[0].strip() for rec in recs]
        results = []
        table_data = []
        for idx, node in enumerate(self.books_ll.iter_nodes(), 1):
            if node.title in titles:
                description = translate_en_to_vi(node.description)
                truncated_desc_split = description.split()
                truncated_description = " ".join(truncated_desc_split[:30]) + "..."
                authors_split = str(node.authors).split(";")
                if len(authors_split) == 2:
                    authors_str = f"{authors_split[0]} and {authors_split[1]}"
                elif len(authors_split) > 2:
                    authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
                else:
                    authors_str = node.authors
                thumbnail = node.thumbnail
                if not isinstance(thumbnail, str) or not thumbnail.startswith("http"):
                    thumbnail = "https://via.placeholder.com/150?text=No+Image"
                caption = f"{node.title} by {authors_str}: {truncated_description}"
                results.append((thumbnail, caption))
                table_data.append([
                    idx,
                    node.title,
                    authors_str,
                    node.categories,
                    description,
                    thumbnail
                ])
                if len(results) >= 16:
                    break
        import pandas as pd
        columns = ["Index", "Title", "Authors", "Category", "Description", "Thumbnail"]
        return results, pd.DataFrame(table_data, columns=columns)