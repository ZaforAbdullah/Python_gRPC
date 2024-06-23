import grpc
import bookstore_pb2
import bookstore_pb2_grpc

def run():
    metadata = [('source', 'client')]  # Define metadata here

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = bookstore_pb2_grpc.BookStoreStub(channel)
        
        # Construct the request message
        request = bookstore_pb2.BookSearch(name='Great')
        
        try:
            # Extract and print server metadata
            response, call = stub.first.with_call(request, metadata=metadata)
            initial_metadata = call.initial_metadata()
            print("Initial Metadata: ", initial_metadata)
            for key, value in initial_metadata:
                print(f"Received metadata from server: {key} = {value}")
            
            print(f'Client received: {response}')
        except grpc.RpcError as e:
            print(f'Error: {e.code()} - {e.details()}')

if __name__ == '__main__':
    run()
