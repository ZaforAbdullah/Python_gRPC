import grpc
from concurrent import futures
import time
import logging

import bookstore_pb2
import bookstore_pb2_grpc

class BookStore(bookstore_pb2_grpc.BookStoreServicer):
    def __init__(self):
        self.book_map = {
            "Great": bookstore_pb2.Book(
                name="Great",
                author="Scott Fitzgerald",
                price=300
            )
        }

    def first(self, request, context):
        print(f"Server received: {request.name}")
        
        # Extract metadata from context
        metadata = context.invocation_metadata()
        for key, value in metadata:
            print(f"Received metadata from: {key} = {value}")
        
        # Send metadata to client
        response_metadata = [('source', 'server')]
        context.send_initial_metadata(response_metadata)
        
        return self.book_map.get(request.name, bookstore_pb2.Book())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bookstore_pb2_grpc.add_BookStoreServicer_to_server(BookStore(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig()
    serve()
