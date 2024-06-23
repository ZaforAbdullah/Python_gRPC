# client_blocking.py

import grpc
from concurrent import futures
import time

import bookstore_pb2
import bookstore_pb2_grpc

class BookStoreClientUnaryBlocking:
    def __init__(self, channel):
        self.stub = bookstore_pb2_grpc.BookStoreStub(channel)

    def get_book(self, book_name):
        print(f"Querying for book with title: {book_name}")
        request = bookstore_pb2.BookSearch(name=book_name)

        try:
            response = self.stub.first(request)
            print(f"Got following book from server: {response}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")

def run():
    server_address = 'localhost:50051'
    with grpc.insecure_channel(server_address) as channel:
        client = BookStoreClientUnaryBlocking(channel)
        book_name = input("Enter book name to search: ")
        client.get_book(book_name)

if __name__ == '__main__':
    run()
