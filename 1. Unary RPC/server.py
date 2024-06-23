from concurrent import futures
import grpc
import random
import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreServicer(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        
        self.books = {
            "The Catcher in the Rye": bookstore_pb2.Book(name="The Catcher in the Rye", author="J.D. Salinger", price=14),
            "The Great Gatsby": bookstore_pb2.Book(name="The Great Gatsby", author="F. Scott Fitzgerald", price=15),
            "To Kill a Mockingbird": bookstore_pb2.Book(name="To Kill a Mockingbird", author="Harper Lee", price=12),
            "1984": bookstore_pb2.Book(name="1984", author="George Orwell", price=10)
        }

    def First(self, request, context):
        matches = [book for name, book in self.books.items() if request.name.lower() in name.lower()]
        if matches:
            return random.choice(matches)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found')
            return bookstore_pb2.Book()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started, listening on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
