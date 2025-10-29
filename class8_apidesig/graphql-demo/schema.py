"""
GraphQL Schema Definition using Strawberry
Demonstrates types, queries, mutations, and relationships
"""

import strawberry
from typing import List, Optional
from models import db


# GraphQL Types (Object Types)
@strawberry.type
class User:
    """User type representing a user in the system"""
    id: int
    username: str
    email: str
    name: str
    age: int
    city: str
    created_at: str

    @strawberry.field
    def posts(self) -> List['Post']:
        """Get all posts by this user - demonstrates relationship resolution"""
        posts_data = db.get_posts_by_author(self.id)
        return [Post(**post) for post in posts_data]

    @strawberry.field
    def comments(self) -> List['Comment']:
        """Get all comments by this user"""
        comments_data = db.get_comments_by_author(self.id)
        return [Comment(**comment) for comment in comments_data]

    @strawberry.field
    def post_count(self) -> int:
        """Computed field: count of user's posts"""
        return len(db.get_posts_by_author(self.id))


@strawberry.type
class Post:
    """Post type representing a blog post"""
    id: int
    title: str
    content: str
    author_id: int
    published: bool
    created_at: str
    likes: int

    @strawberry.field
    def author(self) -> Optional[User]:
        """Get the author of this post - demonstrates nested query"""
        user_data = db.get_user_by_id(self.author_id)
        if user_data:
            return User(**user_data)
        return None

    @strawberry.field
    def comments(self) -> List['Comment']:
        """Get all comments on this post"""
        comments_data = db.get_comments_by_post(self.id)
        return [Comment(**comment) for comment in comments_data]

    @strawberry.field
    def comment_count(self) -> int:
        """Computed field: count of comments"""
        return len(db.get_comments_by_post(self.id))

    @strawberry.field
    def excerpt(self, length: int = 100) -> str:
        """Computed field with argument: post excerpt"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."


@strawberry.type
class Comment:
    """Comment type representing a comment on a post"""
    id: int
    text: str
    author_id: int
    post_id: int
    created_at: str

    @strawberry.field
    def author(self) -> Optional[User]:
        """Get the author of this comment"""
        user_data = db.get_user_by_id(self.author_id)
        if user_data:
            return User(**user_data)
        return None

    @strawberry.field
    def post(self) -> Optional[Post]:
        """Get the post this comment belongs to"""
        post_data = db.get_post_by_id(self.post_id)
        if post_data:
            return Post(**post_data)
        return None


# Input Types (for mutations)
@strawberry.input
class CreateUserInput:
    """Input type for creating a user"""
    username: str
    email: str
    name: str
    age: int
    city: str


@strawberry.input
class CreatePostInput:
    """Input type for creating a post"""
    title: str
    content: str
    author_id: int
    published: bool = True


@strawberry.input
class CreateCommentInput:
    """Input type for creating a comment"""
    text: str
    author_id: int
    post_id: int


@strawberry.input
class UpdatePostInput:
    """Input type for updating a post"""
    post_id: int
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


# Query Type (Read operations)
@strawberry.type
class Query:
    """Root Query type - all read operations"""

    @strawberry.field
    def hello(self) -> str:
        """Simple hello query"""
        return "Hello from GraphQL!"

    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Get a single user by ID"""
        user_data = db.get_user_by_id(id)
        if user_data:
            return User(**user_data)
        return None

    @strawberry.field
    def users(self, limit: Optional[int] = None) -> List[User]:
        """Get all users with optional limit"""
        users_data = db.get_all_users(limit=limit)
        return [User(**user) for user in users_data]

    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        """Get a single post by ID"""
        post_data = db.get_post_by_id(id)
        if post_data:
            return Post(**post_data)
        return None

    @strawberry.field
    def posts(self, published_only: bool = False) -> List[Post]:
        """Get all posts, optionally filter by published status"""
        posts_data = db.get_all_posts(published_only=published_only)
        return [Post(**post) for post in posts_data]

    @strawberry.field
    def search_posts(self, keyword: str) -> List[Post]:
        """Search posts by keyword in title or content"""
        all_posts = db.get_all_posts()
        keyword_lower = keyword.lower()
        filtered = [
            post for post in all_posts
            if keyword_lower in post["title"].lower() or keyword_lower in post["content"].lower()
        ]
        return [Post(**post) for post in filtered]

    @strawberry.field
    def popular_posts(self, min_likes: int = 50) -> List[Post]:
        """Get popular posts with minimum likes"""
        all_posts = db.get_all_posts(published_only=True)
        filtered = [post for post in all_posts if post["likes"] >= min_likes]
        # Sort by likes descending
        filtered.sort(key=lambda x: x["likes"], reverse=True)
        return [Post(**post) for post in filtered]


# Mutation Type (Write operations)
@strawberry.type
class Mutation:
    """Root Mutation type - all write operations"""

    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> User:
        """Create a new user"""
        user_data = db.create_user(
            username=input.username,
            email=input.email,
            name=input.name,
            age=input.age,
            city=input.city
        )
        return User(**user_data)

    @strawberry.mutation
    def create_post(self, input: CreatePostInput) -> Post:
        """Create a new post"""
        post_data = db.create_post(
            title=input.title,
            content=input.content,
            author_id=input.author_id,
            published=input.published
        )
        return Post(**post_data)

    @strawberry.mutation
    def create_comment(self, input: CreateCommentInput) -> Comment:
        """Create a new comment"""
        comment_data = db.create_comment(
            text=input.text,
            author_id=input.author_id,
            post_id=input.post_id
        )
        return Comment(**comment_data)

    @strawberry.mutation
    def update_post(self, input: UpdatePostInput) -> Optional[Post]:
        """Update an existing post"""
        post_data = db.update_post(
            post_id=input.post_id,
            title=input.title,
            content=input.content,
            published=input.published
        )
        if post_data:
            return Post(**post_data)
        return None

    @strawberry.mutation
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        return db.delete_post(post_id)


# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
