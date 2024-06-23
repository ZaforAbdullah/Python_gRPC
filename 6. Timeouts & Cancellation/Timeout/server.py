import grpc
from concurrent import futures
import time
import logging

import bookstore_pb2
import bookstore_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):

    def __init__(self):
        self.book_map = {
            "Great Gatsby": bookstore_pb2.Book(name="Great Gatsby", author="Scott Fitzgerald", price=300),
            "To Kill MockingBird": bookstore_pb2.Book(name="To Kill MockingBird", author="Harper Lee", price=400),
            "Passage to India": bookstore_pb2.Book(name="Passage to India", author="E.M.Forster", price=500),
            "The Side of Paradise": bookstore_pb2.Book(name="The Side of Paradise", author="Scott Fitzgerald", price=600),
            "Go Set a Watchman": bookstore_pb2.Book(name="Go Set a Watchman", author="Harper Lee", price=700)
        }

    def first(self, request, context):
        book_name = request.name.strip()
        logging.info(f"Searching for book with title: {book_name}")
        logging.info("This may take more time...")

        time.sleep(5)  # Simulating delay

        matching_books = [book for book in self.book_map.values() if book.name.startswith(book_name)]
        if matching_books:
            return matching_books[0]
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return bookstore_pb2.Book()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started, listening on port 50051")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
