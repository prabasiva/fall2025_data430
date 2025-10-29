"""
FastAPI + GraphQL Server
Demonstrates integration of GraphQL with FastAPI
"""

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema

# Create FastAPI app
app = FastAPI(
    title="GraphQL Demo API",
    description="A comprehensive GraphQL API demonstrating queries, mutations, and relationships",
    version="1.0.0"
)


# Create GraphQL router
graphql_app = GraphQLRouter(schema)


# Add GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")


# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "GraphQL Demo API",
        "version": "1.0.0",
        "graphql_endpoint": "/graphql",
        "graphql_playground": "/graphql (open in browser)",
        "documentation": {
            "queries": [
                "hello",
                "user(id: Int)",
                "users(limit: Int)",
                "post(id: Int)",
                "posts(publishedOnly: Boolean)",
                "searchPosts(keyword: String)",
                "popularPosts(minLikes: Int)"
            ],
            "mutations": [
                "createUser(input: CreateUserInput)",
                "createPost(input: CreatePostInput)",
                "createComment(input: CreateCommentInput)",
                "updatePost(input: UpdatePostInput)",
                "deletePost(postId: Int)"
            ]
        },
        "example_queries": {
            "simple_query": """
query {
  hello
  users {
    id
    name
    email
  }
}
            """,
            "nested_query": """
query {
  user(id: 1) {
    name
    email
    posts {
      title
      likes
      comments {
        text
        author {
          name
        }
      }
    }
  }
}
            """,
            "mutation_example": """
mutation {
  createPost(input: {
    title: "New Post"
    content: "Post content here"
    authorId: 1
    published: true
  }) {
    id
    title
    author {
      name
    }
  }
}
            """
        }
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GraphQL Demo API"}


if __name__ == "__main__":
    import uvicorn
    print("Starting GraphQL server...")
    print("GraphQL Playground: http://localhost:8000/graphql")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
