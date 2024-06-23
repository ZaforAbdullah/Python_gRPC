import grpc
import bookstore_pb2
import bookstore_pb2_grpc

def run(book_name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bookstore_pb2_grpc.BookStoreStub(channel)
        request = bookstore_pb2.BookSearch(name=book_name)
        try:
            response = stub.First(request)
            print(f"Got book from server: {response.name}, Author: {response.author}, Price: {response.price}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()}, {e.details()}")

if __name__ == '__main__':
    import sys
    book_name = sys.argv[1] if len(sys.argv) > 1 else ""
    run(book_name)
