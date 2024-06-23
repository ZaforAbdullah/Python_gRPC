import grpc
import bookstore_pb2
import bookstore_pb2_grpc
import time
from datetime import datetime

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = bookstore_pb2_grpc.BookStoreStub(channel)

    def generate_books():
        while True:
            book_name = input("Type book name to be added to the cart (type 'EXIT' to finish): ")
            if book_name == 'EXIT':
                break
            yield bookstore_pb2.Book(name=book_name)

    cart = stub.totalCartValue(generate_books())
    print(f"Order summary:\nTotal number of Books: {cart.books}\nTotal Order Value: {cart.price}")

if __name__ == '__main__':
    run()
