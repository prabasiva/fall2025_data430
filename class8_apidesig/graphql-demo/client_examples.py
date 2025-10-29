"""
GraphQL Client Examples
Demonstrates various GraphQL queries and mutations using Python requests
"""

import requests
import json


# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"


def execute_query(query: str, variables: dict = None):
    """Execute a GraphQL query"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(GRAPHQL_URL, json=payload)
    return response.json()


def print_result(title: str, result: dict):
    """Pretty print results"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(json.dumps(result, indent=2))


# Example 1: Simple Query
def example_1_simple_query():
    """Example 1: Simple hello query"""
    query = """
    query {
        hello
    }
    """
    result = execute_query(query)
    print_result("Example 1: Simple Query", result)


# Example 2: Fetch Users
def example_2_fetch_users():
    """Example 2: Fetch all users"""
    query = """
    query {
        users {
            id
            name
            email
            city
        }
    }
    """
    result = execute_query(query)
    print_result("Example 2: Fetch All Users", result)


# Example 3: Fetch Single User with Posts
def example_3_user_with_posts():
    """Example 3: Fetch a user with their posts (nested query)"""
    query = """
    query {
        user(id: 1) {
            id
            name
            email
            postCount
            posts {
                id
                title
                likes
                published
            }
        }
    }
    """
    result = execute_query(query)
    print_result("Example 3: User with Posts", result)


# Example 4: Fetch Post with Author and Comments
def example_4_post_with_relationships():
    """Example 4: Fetch a post with author and comments (deep nesting)"""
    query = """
    query {
        post(id: 1) {
            id
            title
            content
            likes
            author {
                id
                name
                email
            }
            comments {
                id
                text
                author {
                    name
                }
            }
            commentCount
        }
    }
    """
    result = execute_query(query)
    print_result("Example 4: Post with Author and Comments", result)


# Example 5: Query with Variables
def example_5_query_with_variables():
    """Example 5: Query using variables"""
    query = """
    query GetUser($userId: Int!) {
        user(id: $userId) {
            id
            name
            email
            posts {
                title
            }
        }
    }
    """
    variables = {"userId": 2}
    result = execute_query(query, variables)
    print_result("Example 5: Query with Variables", result)


# Example 6: Field Arguments
def example_6_field_arguments():
    """Example 6: Using field arguments (excerpt)"""
    query = """
    query {
        posts(publishedOnly: true) {
            id
            title
            excerpt(length: 50)
            likes
        }
    }
    """
    result = execute_query(query)
    print_result("Example 6: Field Arguments", result)


# Example 7: Search Posts
def example_7_search_posts():
    """Example 7: Search posts by keyword"""
    query = """
    query {
        searchPosts(keyword: "GraphQL") {
            id
            title
            content
            author {
                name
            }
        }
    }
    """
    result = execute_query(query)
    print_result("Example 7: Search Posts", result)


# Example 8: Popular Posts
def example_8_popular_posts():
    """Example 8: Get popular posts"""
    query = """
    query {
        popularPosts(minLikes: 50) {
            id
            title
            likes
            author {
                name
            }
            commentCount
        }
    }
    """
    result = execute_query(query)
    print_result("Example 8: Popular Posts", result)


# Example 9: Create User Mutation
def example_9_create_user():
    """Example 9: Create a new user"""
    mutation = """
    mutation {
        createUser(input: {
            username: "john_doe"
            email: "john@example.com"
            name: "John Doe"
            age: 30
            city: "Boston"
        }) {
            id
            name
            email
            city
        }
    }
    """
    result = execute_query(mutation)
    print_result("Example 9: Create User", result)


# Example 10: Create Post Mutation
def example_10_create_post():
    """Example 10: Create a new post"""
    mutation = """
    mutation {
        createPost(input: {
            title: "Learning GraphQL"
            content: "GraphQL is a powerful query language for APIs."
            authorId: 1
            published: true
        }) {
            id
            title
            author {
                name
            }
            createdAt
        }
    }
    """
    result = execute_query(mutation)
    print_result("Example 10: Create Post", result)


# Example 11: Create Comment Mutation
def example_11_create_comment():
    """Example 11: Create a comment on a post"""
    mutation = """
    mutation {
        createComment(input: {
            text: "This is a great post!"
            authorId: 2
            postId: 1
        }) {
            id
            text
            author {
                name
            }
            post {
                title
            }
        }
    }
    """
    result = execute_query(mutation)
    print_result("Example 11: Create Comment", result)


# Example 12: Update Post Mutation
def example_12_update_post():
    """Example 12: Update an existing post"""
    mutation = """
    mutation {
        updatePost(input: {
            postId: 5
            title: "Updated: Upcoming Features"
            published: true
        }) {
            id
            title
            published
        }
    }
    """
    result = execute_query(mutation)
    print_result("Example 12: Update Post", result)


# Example 13: Complex Query - Multiple Operations
def example_13_multiple_operations():
    """Example 13: Multiple queries in one request"""
    query = """
    query {
        allUsers: users(limit: 3) {
            name
        }
        publishedPosts: posts(publishedOnly: true) {
            title
            likes
        }
        specificUser: user(id: 1) {
            name
            postCount
        }
    }
    """
    result = execute_query(query)
    print_result("Example 13: Multiple Operations", result)


# Example 14: Aliases and Fragments
def example_14_aliases_and_fragments():
    """Example 14: Using aliases"""
    query = """
    query {
        firstUser: user(id: 1) {
            id
            name
            email
        }
        secondUser: user(id: 2) {
            id
            name
            email
        }
    }
    """
    result = execute_query(query)
    print_result("Example 14: Aliases", result)


def run_all_examples():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "GraphQL Client Examples" + " " * 20 + "║")
    print("╚" + "═" * 58 + "╝")

    examples = [
        example_1_simple_query,
        example_2_fetch_users,
        example_3_user_with_posts,
        example_4_post_with_relationships,
        example_5_query_with_variables,
        example_6_field_arguments,
        example_7_search_posts,
        example_8_popular_posts,
        example_9_create_user,
        example_10_create_post,
        example_11_create_comment,
        example_12_update_post,
        example_13_multiple_operations,
        example_14_aliases_and_fragments,
    ]

    for i, example in enumerate(examples, 1):
        try:
            example()
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}")

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    print("Make sure the GraphQL server is running at http://localhost:8000")
    print("Starting in 3 seconds...")
    import time
    time.sleep(3)

    run_all_examples()
