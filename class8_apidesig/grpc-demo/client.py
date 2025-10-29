import grpc
import time
from datetime import datetime
import user_service_pb2
import user_service_pb2_grpc


def run_get_user(stub):
    """Demo: Unary RPC - Get a single user"""
    print("\n" + "=" * 60)
    print("1. UNARY RPC: GetUser")
    print("=" * 60)

    user_id = 1
    print(f"Requesting user with ID: {user_id}")

    try:
        response = stub.GetUser(user_service_pb2.GetUserRequest(user_id=user_id))
        print(f"Response:")
        print(f"  User ID: {response.user_id}")
        print(f"  Name: {response.name}")
        print(f"  Email: {response.email}")
        print(f"  Age: {response.age}")
        print(f"  Created At: {response.created_at}")
    except grpc.RpcError as e:
        print(f"Error: {e.code()} - {e.details()}")


def run_create_user(stub):
    """Demo: Unary RPC - Create a new user"""
    print("\n" + "=" * 60)
    print("2. UNARY RPC: CreateUser")
    print("=" * 60)

    print("Creating new user: John Doe")

    request = user_service_pb2.CreateUserRequest(
        name="John Doe", email="john.doe@example.com", age=32
    )

    response = stub.CreateUser(request)
    print(f"User created successfully!")
    print(f"  User ID: {response.user_id}")
    print(f"  Name: {response.name}")
    print(f"  Email: {response.email}")
    print(f"  Age: {response.age}")
    print(f"  Created At: {response.created_at}")


def run_list_users(stub):
    """Demo: Server streaming RPC - List users"""
    print("\n" + "=" * 60)
    print("3. SERVER STREAMING RPC: ListUsers")
    print("=" * 60)

    limit = 3
    print(f"Requesting {limit} users (streaming)...")

    request = user_service_pb2.ListUsersRequest(limit=limit)
    responses = stub.ListUsers(request)

    count = 0
    for response in responses:
        count += 1
        print(f"\nUser #{count}:")
        print(f"  User ID: {response.user_id}")
        print(f"  Name: {response.name}")
        print(f"  Email: {response.email}")
        print(f"  Age: {response.age}")


def run_batch_create_users(stub):
    """Demo: Client streaming RPC - Batch create users"""
    print("\n" + "=" * 60)
    print("4. CLIENT STREAMING RPC: BatchCreateUsers")
    print("=" * 60)

    print("Streaming multiple user creation requests...")

    def generate_user_requests():
        users = [
            {"name": "Frank Miller", "email": "frank@example.com", "age": 45},
            {"name": "Grace Lee", "email": "grace@example.com", "age": 29},
            {"name": "Henry Davis", "email": "henry@example.com", "age": 38},
        ]

        for user in users:
            print(f"  Sending: {user['name']}")
            yield user_service_pb2.CreateUserRequest(
                name=user["name"], email=user["email"], age=user["age"]
            )
            time.sleep(0.3)  # Simulate delay

    response = stub.BatchCreateUsers(generate_user_requests())
    print(f"\nBatch creation completed!")
    print(f"  Total users created: {response.users_created}")
    print(f"  User IDs: {list(response.user_ids)}")


def run_stream_users(stub):
    """Demo: Bidirectional streaming RPC - Chat-like messaging"""
    print("\n" + "=" * 60)
    print("5. BIDIRECTIONAL STREAMING RPC: StreamUsers")
    print("=" * 60)

    print("Starting bidirectional stream...")

    def generate_messages():
        messages = [
            {"user_id": 1, "message": "Hello from client!"},
            {"user_id": 1, "message": "How are you?"},
            {"user_id": 2, "message": "gRPC is awesome!"},
        ]

        for msg in messages:
            print(f"\nSending: User {msg['user_id']}: {msg['message']}")
            yield user_service_pb2.UserMessage(
                user_id=msg["user_id"],
                message=msg["message"],
                timestamp=datetime.now().isoformat(),
            )
            time.sleep(0.5)

    responses = stub.StreamUsers(generate_messages())

    for response in responses:
        print(f"Received: User {response.user_id}: {response.message}")


def run_all_demos(stub):
    """Run all demo functions"""
    demos = [
        run_get_user,
        run_create_user,
        run_list_users,
        run_batch_create_users,
        run_stream_users,
    ]

    for demo in demos:
        demo(stub)
        time.sleep(1)  # Pause between demos

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


def run():
    """Main client function"""
    server_address = "localhost:50051"
    print(f"Connecting to gRPC server at {server_address}...")

    # Create a channel and stub
    with grpc.insecure_channel(server_address) as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)

        print("Connected successfully!")

        # Run all demos
        run_all_demos(stub)


if __name__ == "__main__":
    run()
