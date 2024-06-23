import grpc
import asyncio
import logging

from bookstore_pb2 import Book
from bookstore_pb2_grpc import BookStoreStub

class BookStoreClient:
    def __init__(self, channel):
        self.stub = BookStoreStub(channel)
        self.call = None

    async def get_server_response(self):
        try:
            response = await self.call
            logging.info("Order summary:\nTotal number of Books: %d\nTotal Order Value: %d", response.books, response.price)
        except grpc.aio.AioRpcError as e:
            logging.error("Error while reading response from Server: %s", e)

    async def add_book(self, book):
        logging.info("Adding book with title starting with: %s", book)
        request = Book(name=book)

        if self.call is None:
            self.call = self.stub.totalCartValue()

        try:
            await self.call.write(request)
        except grpc.aio.AioRpcError as e:
            logging.error("Error sending request: %s", e)

    async def complete_order(self):
        logging.info("Done, waiting for server to create order summary...")
        if self.call is not None:
            await self.call.done_writing()
            await self.get_server_response()

    async def cancel_order(self):
        logging.info("Cancelling the order...")
        if self.call is not None:
            self.call.cancel()

async def main():
    logging.basicConfig(level=logging.INFO)
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        client = BookStoreClient(channel)
        while True:
            book_name = input("Type book name to be added to the cart (type 'EXIT' to complete order or 'CANCEL' to cancel order): ").strip()
            if book_name == 'EXIT':
                await client.complete_order()
                break
            elif book_name == 'CANCEL':
                await client.cancel_order()
                break
            else:
                await client.add_book(book_name)

if __name__ == '__main__':
    asyncio.run(main())
