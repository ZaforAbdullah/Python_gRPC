import grpc
import bookstore_pb2
import bookstore_pb2_grpc
import time
from datetime import datetime

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = bookstore_pb2_grpc.BookStoreStub(channel)

    try:
        book_names = ["Great", "To", "Passage", "Go"]
        responses = stub.liveCartValue(generate_requests(book_names))
        for response in responses:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] \nOrder summary:\nTotal number of Books: {response.books}\nTotal Order Value: {response.price}")

    except grpc.RpcError as e:
        print(f"RPC failed: {e}")

def generate_requests(book_names):
    for name in book_names:
        time.sleep(2)
        yield bookstore_pb2.Book(name=name)

if __name__ == '__main__':
    run()
