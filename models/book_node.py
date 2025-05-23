class BookNode:
    def __init__(self, isbn13, isbn10, title, authors, categories, thumbnail, description,
                published_year, average_rating, num_pages, ratings_count,
                title_and_subtitle, tagged_description, next=None):
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
        self.next = next