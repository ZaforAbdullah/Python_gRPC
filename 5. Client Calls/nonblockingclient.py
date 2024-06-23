import bookstore_pb2
import bookstore_pb2_grpc
import grpc
import time
import logging
import threading
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ServerResponseObserver:
    def __init__(self, author):
        self.author = author

    def __call__(self, response):
        logger.info(f"Server returned book by {self.author}: {response}")

    def on_error(self, error):
        logger.error(f"Error while reading response from Server: {error}")

    def on_completed(self):
        logger.info(f"Server stream for {self.author} completed.")

class BookStoreClient:
    def __init__(self, channel):
        self.stub = bookstore_pb2_grpc.BookStoreStub(channel)
        self.logger = logging.getLogger(__name__)

    def get_server_response_observer(self, author):
        return ServerResponseObserver(author)

    def get_book_with_observer(self, author, timeout=100):
        timestamp_start = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp_start}]")
        self.logger.debug(f"Querying for book with author: {author}")
        request = bookstore_pb2.BookSearch(author=author)

        try:
            response_stream = self.stub.searchByAuthor(request, timeout=timeout)
            response_observer = self.get_server_response_observer(author)
            for response in response_stream:
                response_observer(response)
            timestamp_end= datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp_end}]")
        except grpc.RpcError as e:
            self.logger.error(f"RPC failed: {e}")
        except Exception as ex:
            self.logger.error(f"Unexpected error: {ex}")

def run():
    server_address = 'localhost:50051'
    channel = grpc.insecure_channel(server_address)
    client = BookStoreClient(channel)

    author_names = ["Scott Fitzgerald", "Harper Lee", "E.M.Forster"]

    threads = []
    for author in author_names:
        thread = threading.Thread(target=client.get_book_with_observer, args=(author,))
        thread.start()
        time.sleep(3)  # Introduce delay for demonstration
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    channel.close()

if __name__ == '__main__':
    run()