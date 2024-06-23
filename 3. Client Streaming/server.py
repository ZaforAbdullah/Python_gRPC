from concurrent import futures
import grpc
import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        self.book_map = {
            "Great Gatsby": bookstore_pb2.Book(name="Great Gatsby", author="Scott Fitzgerald", price=300),
            "To Kill a MockingBird": bookstore_pb2.Book(name="To Kill a MockingBird", author="Harper Lee", price=400),
            "Passage to India": bookstore_pb2.Book(name="Passage to India", author="E.M.Forster", price=500),
            "The Side of Paradise": bookstore_pb2.Book(name="The Side of Paradise", author="Scott Fitzgerald", price=600),
            "Go Set a Watchman": bookstore_pb2.Book(name="Go Set a Watchman", author="Harper Lee", price=700),
        }

    def totalCartValue(self, request_iterator, context):
        cart_books = []
        for book in request_iterator:
            print(f"Searching for book with title starting with: {book.name}")
            for book_entry in self.book_map.values():
                if book_entry.name.startswith(book.name):
                    print(f"Found book, adding to cart: {book_entry.name}")
                    cart_books.append(book_entry)
        
        total_price = sum(book.price for book in cart_books)
        return bookstore_pb2.Cart(books=len(cart_books), price=total_price)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
