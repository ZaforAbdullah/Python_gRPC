import grpc
import bookstore_pb2
import bookstore_pb2_grpc
from datetime import datetime
def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = bookstore_pb2_grpc.BookStoreStub(channel)
    try:
        response = stub.searchByAuthor(bookstore_pb2.BookSearch(author='Har'))
        for book in response:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Received book: {book.name} by {book.author}, Price: ${book.price}")
    except grpc.RpcError as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    run()
