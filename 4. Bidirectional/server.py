import grpc
from concurrent import futures
import time
from datetime import datetime

import bookstore_pb2
import bookstore_pb2_grpc

# Define the server class
class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):

    def __init__(self):
        self.book_map = {
            "Great Gatsby": bookstore_pb2.Book(name="Great Gatsby", author="Scott Fitzgerald", price=300),
            "To Kill MockingBird": bookstore_pb2.Book(name="To Kill MockingBird", author="Harper Lee", price=400),
            "Passage to India": bookstore_pb2.Book(name="Passage to India", author="E.M.Forster", price=500),
            "The Side of Paradise": bookstore_pb2.Book(name="The Side of Paradise", author="Scott Fitzgerald", price=600),
            "Go Set a Watchman": bookstore_pb2.Book(name="Go Set a Watchman", author="Harper Lee", price=700)
        }

    def liveCartValue(self, request_iterator, context):
        book_cart = []
        cart_value = 0

        for book in request_iterator:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}]")
            print(f"Searching for book with title starting with: {book.name}")
            for name, stored_book in self.book_map.items():
                if stored_book.name.startswith(book.name):
                    print(f"Found book, adding to cart: {stored_book.name}")
                    book_cart.append(stored_book)
                    cart_value += stored_book.price
            time.sleep(2)
            yield bookstore_pb2.Cart(books=len(book_cart), price=cart_value)
            print(f"Updated cart value: {cart_value}")

        print("Order completed")

# Set up the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051...")
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()