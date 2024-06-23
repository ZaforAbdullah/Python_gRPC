import grpc
from concurrent import futures
import time
import logging

import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        self.book_map = {
            "Great Gatsby": bookstore_pb2.Book(name="Great Gatsby", author="Scott Fitzgerald", price=300),
            "To Kill MockingBird": bookstore_pb2.Book(name="To Kill MockingBird", author="Harper Lee", price=400),
            "Passage to India": bookstore_pb2.Book(name="Passage to India", author="E.M.Forster", price=500),
            "The Side of Paradise": bookstore_pb2.Book(name="The Side of Paradise", author="Scott Fitzgerald", price=600),
            "Go Set a Watchman": bookstore_pb2.Book(name="Go Set a Watchman", author="Harper Lee", price=700)
        }
        self.logger = logging.getLogger(__name__)  # Initialize logger for this class

    def first(self, request, context):
        book_name = request.name
        if book_name in self.book_map:
            return self.book_map[book_name]
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Book '{book_name}' not found.")
            return bookstore_pb2.Book()  # Return an empty book

    def searchByAuthor(self, request, context):
        self.logger.debug(f"Received search request for author: {request.author}")
        found_books = 0
        for book in self.book_map.values():
            if book.author.startswith(request.author):
                found_books += 1
                time.sleep(3)  # Simulating delay
                self.logger.debug(f"Sending book: {book}")
                yield book
        if found_books == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"No books found for author '{request.author}'.")


def serve():
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
    logger = logging.getLogger(__name__)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Server started. Listening on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
