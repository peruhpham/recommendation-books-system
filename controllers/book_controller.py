import pandas as pd
from models.book_linked_list import BookLinkedList
from utils.translation import translate_vi_to_en, translate_en_to_vi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

import time
import tracemalloc

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
        tracemalloc.start()
        # Đo thời gian thực hiện load_books
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu load_books lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

        df = pd.read_csv(self.file_path, encoding='utf-8', sep=',')
        for _, row in df.iterrows():
            thumb = row.get("thumbnail", "")
            if not isinstance(thumb, str) or not thumb.startswith("http"):
                thumb = "https://www.wp-assistance.fr/files/2023/05/erreur-404-WordPress.jpg"
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
        end_time = time.time()
        print(f"[LLM] load_books hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện load_books: {end_time - start_time:.4f} giây")
        print(f"[LLM] Số lượng sách trong linked list: {len(self.books_ll)}")

        current, peak = tracemalloc.get_traced_memory()
        print(f"[LLM] Bộ nhớ đang dùng sau load_books: {current / 1024 / 1024:.2f} MB; Đỉnh: {peak / 1024 / 1024:.2f} MB")
        tracemalloc.stop()

    def build_vector_db(self):
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu build_vector_db lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

        documents = [Document(page_content=f"{node.title} - {node.description}") for node in self.books_ll.iter_nodes()]
        self.db_books = Chroma.from_documents(documents, embedding=self.embedding_model)

        end_time = time.time()
        print(f"[LLM] build_vector_db hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện build_vector_db: {end_time - start_time:.4f} giây")

    def save_books_to_csv(self):
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu save_books_to_csv lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

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
        end_time = time.time()
        print(f"[LLM] save_books_to_csv hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện save_books_to_csv: {end_time - start_time:.4f} giây")
        print(f"[LLM] Số lượng sách trong linked list: {len(self.books_ll)}")
    
    def add_book(self, *args):
        (table, isbn13, isbn10, title, authors, categories, thumbnail, description,
        published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description) = args
        title_en = translate_vi_to_en(title)
        description_en = translate_vi_to_en(description)

        tracemalloc.start()
        # Đo thời gian thực hiện add_book
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu add_book lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        
        self.books_ll.append(
            isbn13, isbn10, title_en, authors, categories, thumbnail, description_en,
            published_year, average_rating, num_pages, ratings_count, title_and_subtitle, tagged_description
        )
        end_time = time.time()
        print(f"[LLM] add_book hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện add_book: {end_time - start_time:.4f} giây")

        self.added_count += 1
        content = f"{title_en} - {description_en}"
        self.db_books.add_documents([Document(page_content=content)])
        self.save_books_to_csv()

        current, peak = tracemalloc.get_traced_memory()
        print(f"[LLM] Bộ nhớ đang dùng sau add_book: {current / 1024 / 1024:.2f} MB; Đỉnh: {peak / 1024 / 1024:.2f} MB")
        tracemalloc.stop()
        return self.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"]), self.get_stats()

    def delete_book(self, table, row_idx):
        tracemalloc.start()
        # Đo thời gian thực hiện delete_book
        print("\nĐo thời gian xóa sách:", row_idx)
        start_time = time.time()
        print(f"[LLM] Bắt đầu delete_book lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

        self.books_ll.delete(int(row_idx))

        end_time = time.time()
        print(f"[LLM] delete_book hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện delete_book: {end_time - start_time:.4f} giây")

        current, peak = tracemalloc.get_traced_memory()
        print(f"[LLM] Bộ nhớ đang dùng sau delete_book: {current / 1024 / 1024:.2f} MB; Đỉnh: {peak / 1024 / 1024:.2f} MB")
        tracemalloc.stop()

        self.deleted_count += 1
        self.save_books_to_csv()
        return self.show_books_table(), self.get_stats()

    # def search_books(self, title, authors, categories):
    #     query = {}
    #     if title: query["title"] = title
    #     if authors: query["authors"] = authors
    #     if categories: query["categories"] = categories
    #     results = self.books_ll.search(query)
    #     # Chuyển results thành DataFrame hoặc list phù hợp với books_table
    #     return pd.DataFrame(results)

    #Tìm kiếm sách theo trường thông tin và giá trị nhập vào trả về list các list
    def search_books(self, field, value):
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu search_books lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        # self.books_ll = BookLinkedList()
        # self.load_books()
        # print("Hiển thị 5 giá trị đầu tiên trong linked list:", self.books_ll.to_list()[:5])
        # Kiểm tra nếu không có giá trị nào được nhập vào
        if not field or not value:
            # Trả về 1 dòng trống đúng thứ tự cột
            return [["", "", "", "Không tìm thấy thông tin!", "", "", "", ""]]
        res = self.books_ll.search(field, value)
        if not res:
            return [["", "", "", "Không tìm thấy thông tin!", "", "", "", ""]]

        end_time = time.time()
        print(f"[LLM] search_books hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện search_books: {end_time - start_time:.4f} giây")
        return res
    
    # def search_books_by_field(self, field, value):
    #     if not value:
    #         return self.show_books_table(columns=["Index", "title", "authors", "description", "thumbnail"])
        
    #     # Truyền đúng tham số cho hàm search
    #     results = self.books_ll.search(field, value)
        
    #     if not results:
    #         return pd.DataFrame([{
    #             "Index": "",
    #             "title": "Không tìm thấy thông tin!",
    #             "authors": "",
    #             "description": "",
    #             "thumbnail": ""
    #         }])
        
    #     return pd.DataFrame(results)

    
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
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu show_books_table lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        all_books = self.books_ll.to_list()
        end_time = time.time()
        print(f"[LLM] show_books_table hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện show_books_table: {end_time - start_time:.4f} giây")

        if not all_books:
            return []
        if columns:
            return [[book.get(col, "") for col in columns] for book in all_books]
        return [[book.get(col, "") for col in all_books[0].keys()] for book in all_books]

    def recommend_books(self, query):
        start_time = time.time()
        print(f"\n[LLM] Bắt đầu recommend_books lúc: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

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
                    thumbnail = "https://www.wp-assistance.fr/files/2023/05/erreur-404-WordPress.jpg"
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
        
        end_time = time.time()
        print(f"[LLM] recommend_books hoàn thành lúc: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"[LLM] Thời gian thực hiện recommend_books: {end_time - start_time:.4f} giây")
    
        return results, pd.DataFrame(table_data, columns=columns)

# print("Số lượng sách trong linked list:", len(self.books_ll))