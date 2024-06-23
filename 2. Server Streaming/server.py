import grpc
from concurrent import futures
import time
import logging

import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        self.books = {
            "Great Gatsby": bookstore_pb2.Book(name="Great Gatsby", author="Scott Fitzgerald", price=300),
            "To Kill MockingBird": bookstore_pb2.Book(name="To Kill MockingBird", author="Harper Lee", price=400),
            "Passage to India": bookstore_pb2.Book(name="Passage to India", author="E.M.Forster", price=500),
            "The Side of Paradise": bookstore_pb2.Book(name="The Side of Paradise", author="Scott Fitzgerald", price=600),
            "Go Set a Watchman": bookstore_pb2.Book(name="Go Set a Watchman", author="Harper Lee", price=700)
        }
    
    def searchByAuthor(self, request, context):
        author_prefix = request.author.lower()
        for book_name, book in self.books.items():
            if author_prefix in book.author.lower():
                yield book
                time.sleep(3)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()
