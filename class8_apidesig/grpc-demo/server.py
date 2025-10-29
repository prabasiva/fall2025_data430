import grpc
from concurrent import futures
import time
from datetime import datetime
import user_service_pb2
import user_service_pb2_grpc


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    """Implementation of UserService gRPC service"""

    def __init__(self):
        # In-memory storage for demo purposes
        self.users = {}
        self.next_user_id = 1

        # Add some sample users
        self._add_sample_users()

    def _add_sample_users(self):
        """Add sample users for testing"""
        sample_users = [
            {"name": "Alice Johnson", "email": "alice@example.com", "age": 28},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35},
            {"name": "Charlie Brown", "email": "charlie@example.com", "age": 42},
            {"name": "Diana Prince", "email": "diana@example.com", "age": 30},
            {"name": "Eve Wilson", "email": "eve@example.com", "age": 25},
        ]

        for user_data in sample_users:
            user_id = self.next_user_id
            self.users[user_id] = {
                "user_id": user_id,
                "name": user_data["name"],
                "email": user_data["email"],
                "age": user_data["age"],
                "created_at": datetime.now().isoformat(),
            }
            self.next_user_id += 1

    def GetUser(self, request, context):
        """Unary RPC: Get a single user by ID"""
        print(f"GetUser called for user_id: {request.user_id}")

        if request.user_id not in self.users:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User with ID {request.user_id} not found")
            return user_service_pb2.UserResponse()

        user = self.users[request.user_id]
        return user_service_pb2.UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            age=user["age"],
            created_at=user["created_at"],
        )

    def CreateUser(self, request, context):
        """Unary RPC: Create a new user"""
        print(f"CreateUser called for: {request.name}")

        user_id = self.next_user_id
        self.users[user_id] = {
            "user_id": user_id,
            "name": request.name,
            "email": request.email,
            "age": request.age,
            "created_at": datetime.now().isoformat(),
        }
        self.next_user_id += 1

        user = self.users[user_id]
        return user_service_pb2.UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            age=user["age"],
            created_at=user["created_at"],
        )

    def ListUsers(self, request, context):
        """Server streaming RPC: Stream multiple users"""
        print(f"ListUsers called with limit: {request.limit}")

        limit = request.limit if request.limit > 0 else len(self.users)
        count = 0

        for user_id, user in self.users.items():
            if count >= limit:
                break

            yield user_service_pb2.UserResponse(
                user_id=user["user_id"],
                name=user["name"],
                email=user["email"],
                age=user["age"],
                created_at=user["created_at"],
            )
            count += 1
            time.sleep(0.5)  # Simulate delay for streaming effect

    def BatchCreateUsers(self, request_iterator, context):
        """Client streaming RPC: Batch create multiple users"""
        print("BatchCreateUsers called")

        created_ids = []

        for request in request_iterator:
            user_id = self.next_user_id
            self.users[user_id] = {
                "user_id": user_id,
                "name": request.name,
                "email": request.email,
                "age": request.age,
                "created_at": datetime.now().isoformat(),
            }
            created_ids.append(user_id)
            self.next_user_id += 1
            print(f"  Created user: {request.name} with ID: {user_id}")

        return user_service_pb2.BatchCreateResponse(
            users_created=len(created_ids), user_ids=created_ids
        )

    def StreamUsers(self, request_iterator, context):
        """Bidirectional streaming RPC: Chat-like messaging"""
        print("StreamUsers called (bidirectional streaming)")

        for message in request_iterator:
            print(f"  Received message from user {message.user_id}: {message.message}")

            # Echo back with server response
            response = user_service_pb2.UserMessage(
                user_id=0,  # 0 represents the server
                message=f"Server received: {message.message}",
                timestamp=datetime.now().isoformat(),
            )
            yield response


def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )

    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"gRPC Server started on port {port}")
    print("Server is ready to accept requests...")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(0)


if __name__ == "__main__":
    serve()
