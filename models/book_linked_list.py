from .book_node import BookNode

class BookLinkedList:
    def __init__(self):
        self.head = None

    def append(
    self, isbn13="", isbn10="", title="", authors="", categories="", thumbnail="", description="",
    published_year="", average_rating="", num_pages="", ratings_count="",
    title_and_subtitle="", tagged_description=""
    ):
        new_node = BookNode(
            isbn13, isbn10, title, authors, categories, thumbnail, description,
            published_year, average_rating, num_pages, ratings_count,
            title_and_subtitle, tagged_description
        )
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, index):
        if index < 0:
            raise IndexError("Index không hợp lệ")
        if self.head is None:
            raise ValueError("Danh sách rỗng")

        if index == 0:
            self.head = self.head.next
            return

        current = self.head
        for _ in range(index - 1):
            if current is None or current.next is None:
                raise IndexError("Index không hợp lệ")
            current = current.next

        if current.next is None:
            raise IndexError("Index không hợp lệ")

        current.next = current.next.next


    def to_list(self):
        result = []
        current = self.head
        idx = 1
        while current:
            result.append({
                "Index": idx,
                "isbn13": current.isbn13,
                "isbn10": current.isbn10,
                "title": current.title,
                "authors": current.authors,
                "categories": current.categories,
                "thumbnail": current.thumbnail,
                "description": current.description,
                "published_year": current.published_year,
                "average_rating": current.average_rating,
                "num_pages": current.num_pages,
                "ratings_count": current.ratings_count,
                "title_and_subtitle": current.title_and_subtitle,
                "tagged_description": current.tagged_description,
                "content": f"{current.title} - {current.description}"
            })
            current = current.next
            idx += 1
        return result

    """
    Lợi ích của yield trong trường hợp này
    Tiết kiệm bộ nhớ:

    Không cần lưu toàn bộ các nút vào một danh sách trung gian như to_list() trước khi xử lý.

    Chỉ giữ trạng thái nút hiện tại.

    Hiệu quả với danh sách lớn:

    Thích hợp để xử lý dữ liệu lớn vì không yêu cầu tải tất cả nút vào bộ nhớ cùng lúc."""
    def iter_nodes(self):
        current = self.head  
        
        while current:  
            # Trả về nút hiện tại dưới dạng generator
            yield current  
            
            current = current.next  


    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    # có thể bổ sung các hàm update, delete như trước
