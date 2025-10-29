"""
Data models for GraphQL demo
Demonstrates relationships between Users, Posts, and Comments
"""

from typing import List, Optional
from datetime import datetime


# In-memory database simulation
class Database:
    def __init__(self):
        self.users: List[dict] = []
        self.posts: List[dict] = []
        self.comments: List[dict] = []
        self._init_data()

    def _init_data(self):
        """Initialize sample data"""

        # Sample users
        self.users = [
            {
                "id": 1,
                "username": "alice_smith",
                "email": "alice@example.com",
                "name": "Alice Smith",
                "age": 28,
                "city": "San Francisco",
                "created_at": "2024-01-15T10:00:00"
            },
            {
                "id": 2,
                "username": "bob_jones",
                "email": "bob@example.com",
                "name": "Bob Jones",
                "age": 35,
                "city": "New York",
                "created_at": "2024-02-20T14:30:00"
            },
            {
                "id": 3,
                "username": "carol_white",
                "email": "carol@example.com",
                "name": "Carol White",
                "age": 42,
                "city": "Los Angeles",
                "created_at": "2024-03-10T09:15:00"
            },
            {
                "id": 4,
                "username": "david_brown",
                "email": "david@example.com",
                "name": "David Brown",
                "age": 31,
                "city": "Chicago",
                "created_at": "2024-04-05T16:45:00"
            },
            {
                "id": 5,
                "username": "eve_wilson",
                "email": "eve@example.com",
                "name": "Eve Wilson",
                "age": 26,
                "city": "Seattle",
                "created_at": "2024-05-12T11:20:00"
            }
        ]

        # Sample posts
        self.posts = [
            {
                "id": 1,
                "title": "Introduction to GraphQL",
                "content": "GraphQL is a query language for APIs that provides a complete description of the data in your API.",
                "author_id": 1,
                "published": True,
                "created_at": "2024-06-01T10:00:00",
                "likes": 42
            },
            {
                "id": 2,
                "title": "Building REST APIs",
                "content": "REST is an architectural style for designing networked applications.",
                "author_id": 1,
                "published": True,
                "created_at": "2024-06-05T14:30:00",
                "likes": 35
            },
            {
                "id": 3,
                "title": "Getting Started with FastAPI",
                "content": "FastAPI is a modern, fast web framework for building APIs with Python.",
                "author_id": 2,
                "published": True,
                "created_at": "2024-06-10T09:15:00",
                "likes": 58
            },
            {
                "id": 4,
                "title": "Database Design Best Practices",
                "content": "Learn how to design efficient and scalable databases.",
                "author_id": 3,
                "published": True,
                "created_at": "2024-06-15T11:45:00",
                "likes": 27
            },
            {
                "id": 5,
                "title": "Draft: Upcoming Features",
                "content": "This is a draft post about upcoming features.",
                "author_id": 2,
                "published": False,
                "created_at": "2024-06-20T16:30:00",
                "likes": 0
            },
            {
                "id": 6,
                "title": "Python Type Hints Explained",
                "content": "Understanding and using type hints in Python for better code quality.",
                "author_id": 4,
                "published": True,
                "created_at": "2024-06-25T13:20:00",
                "likes": 64
            },
            {
                "id": 7,
                "title": "Microservices Architecture",
                "content": "Breaking down monolithic applications into microservices.",
                "author_id": 5,
                "published": True,
                "created_at": "2024-07-01T10:10:00",
                "likes": 51
            }
        ]

        # Sample comments
        self.comments = [
            {
                "id": 1,
                "text": "Great introduction! Very helpful.",
                "author_id": 2,
                "post_id": 1,
                "created_at": "2024-06-02T11:00:00"
            },
            {
                "id": 2,
                "text": "Thanks for sharing this.",
                "author_id": 3,
                "post_id": 1,
                "created_at": "2024-06-02T15:30:00"
            },
            {
                "id": 3,
                "text": "Could you explain more about resolvers?",
                "author_id": 4,
                "post_id": 1,
                "created_at": "2024-06-03T09:45:00"
            },
            {
                "id": 4,
                "text": "REST is still relevant in 2024!",
                "author_id": 3,
                "post_id": 2,
                "created_at": "2024-06-06T10:20:00"
            },
            {
                "id": 5,
                "text": "FastAPI is amazing for rapid development.",
                "author_id": 1,
                "post_id": 3,
                "created_at": "2024-06-11T14:00:00"
            },
            {
                "id": 6,
                "text": "I've been using FastAPI for a year now, love it!",
                "author_id": 5,
                "post_id": 3,
                "created_at": "2024-06-11T16:30:00"
            },
            {
                "id": 7,
                "text": "What about NoSQL databases?",
                "author_id": 2,
                "post_id": 4,
                "created_at": "2024-06-16T09:15:00"
            },
            {
                "id": 8,
                "text": "Type hints have improved my code quality significantly.",
                "author_id": 3,
                "post_id": 6,
                "created_at": "2024-06-26T11:45:00"
            }
        ]

    # Query methods
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID"""
        return next((u for u in self.users if u["id"] == user_id), None)

    def get_all_users(self, limit: Optional[int] = None) -> List[dict]:
        """Get all users with optional limit"""
        if limit:
            return self.users[:limit]
        return self.users

    def get_post_by_id(self, post_id: int) -> Optional[dict]:
        """Get post by ID"""
        return next((p for p in self.posts if p["id"] == post_id), None)

    def get_all_posts(self, published_only: bool = False) -> List[dict]:
        """Get all posts, optionally filter by published status"""
        if published_only:
            return [p for p in self.posts if p["published"]]
        return self.posts

    def get_posts_by_author(self, author_id: int) -> List[dict]:
        """Get all posts by an author"""
        return [p for p in self.posts if p["author_id"] == author_id]

    def get_comments_by_post(self, post_id: int) -> List[dict]:
        """Get all comments for a post"""
        return [c for c in self.comments if c["post_id"] == post_id]

    def get_comments_by_author(self, author_id: int) -> List[dict]:
        """Get all comments by an author"""
        return [c for c in self.comments if c["author_id"] == author_id]

    # Mutation methods
    def create_user(self, username: str, email: str, name: str, age: int, city: str) -> dict:
        """Create a new user"""
        new_id = max([u["id"] for u in self.users]) + 1 if self.users else 1
        user = {
            "id": new_id,
            "username": username,
            "email": email,
            "name": name,
            "age": age,
            "city": city,
            "created_at": datetime.now().isoformat()
        }
        self.users.append(user)
        return user

    def create_post(self, title: str, content: str, author_id: int, published: bool = True) -> dict:
        """Create a new post"""
        new_id = max([p["id"] for p in self.posts]) + 1 if self.posts else 1
        post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author_id": author_id,
            "published": published,
            "created_at": datetime.now().isoformat(),
            "likes": 0
        }
        self.posts.append(post)
        return post

    def create_comment(self, text: str, author_id: int, post_id: int) -> dict:
        """Create a new comment"""
        new_id = max([c["id"] for c in self.comments]) + 1 if self.comments else 1
        comment = {
            "id": new_id,
            "text": text,
            "author_id": author_id,
            "post_id": post_id,
            "created_at": datetime.now().isoformat()
        }
        self.comments.append(comment)
        return comment

    def update_post(self, post_id: int, title: Optional[str] = None,
                   content: Optional[str] = None, published: Optional[bool] = None) -> Optional[dict]:
        """Update a post"""
        post = self.get_post_by_id(post_id)
        if not post:
            return None

        if title is not None:
            post["title"] = title
        if content is not None:
            post["content"] = content
        if published is not None:
            post["published"] = published

        return post

    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        post = self.get_post_by_id(post_id)
        if post:
            self.posts.remove(post)
            # Also delete related comments
            self.comments = [c for c in self.comments if c["post_id"] != post_id]
            return True
        return False


# Global database instance
db = Database()
