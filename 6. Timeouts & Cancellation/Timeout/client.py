import grpc
import bookstore_pb2
import bookstore_pb2_grpc
import logging

def get_book(book_name):
    channel = grpc.insecure_channel('localhost:50051')
    stub = bookstore_pb2_grpc.BookStoreStub(channel)
    
    try:
        response = stub.first(bookstore_pb2.BookSearch(name=book_name), timeout=2)
        logging.info(f"Got following book from server: {response}")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            logging.warning("Deadline exceeded. Request cancelled.")
        else:
            logging.error(f"RPC failed: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    book_name = input("Enter book name to search: ")
    get_book(book_name)

if __name__ == '__main__':
    main()
