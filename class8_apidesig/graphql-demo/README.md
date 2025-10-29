# GraphQL Demo with FastAPI

A comprehensive GraphQL implementation using Python, FastAPI, and Strawberry GraphQL. This demo showcases queries, mutations, relationships, and best practices.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [GraphQL Schema](#graphql-schema)
- [Example Queries](#example-queries)
- [API Documentation](#api-documentation)
- [Learning Resources](#learning-resources)

## ✨ Features

### Core GraphQL Features
- ✅ **Queries**: Read operations with nested relationships
- ✅ **Mutations**: Create, update, and delete operations
- ✅ **Strong Typing**: Type-safe schema with validation
- ✅ **Relationships**: Users → Posts → Comments
- ✅ **Computed Fields**: Dynamic fields with logic
- ✅ **Field Arguments**: Parameterized fields
- ✅ **Variables**: Dynamic query parameters
- ✅ **Aliases**: Query same field multiple times
- ✅ **Search & Filtering**: Advanced query capabilities

### Implementation Features
- 📦 In-memory database with sample data
- 🎨 Interactive GraphQL Playground
- 📚 Auto-generated documentation
- 🔧 FastAPI integration
- 🐍 Python type hints throughout
- 📝 Comprehensive examples

## 📁 Project Structure

```
graphql-demo/
├── main.py                  # FastAPI + GraphQL server
├── schema.py                # GraphQL schema (types, queries, mutations)
├── models.py                # Data models and in-memory database
├── client_examples.py       # Python client examples
├── requirements.txt         # Dependencies
├── README.md               # This file
├── GRAPHQL_EXPLAINED.md    # Comprehensive GraphQL guide
└── SAMPLE_QUERIES.md       # Collection of example queries
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Navigate to the demo directory
cd graphql-demo

# Install required packages
pip install -r requirements.txt
```

**Dependencies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `strawberry-graphql[fastapi]` - GraphQL library
- `pydantic` - Data validation

## ⚡ Quick Start

### Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Access GraphQL Playground

Open your browser and navigate to:
```
http://localhost:8000/graphql
```

You'll see an interactive GraphQL playground where you can:
- Write and execute queries
- Explore the schema
- View documentation
- Test mutations

### Try Your First Query

In the GraphQL Playground, paste this query:

```graphql
query {
  hello
  users {
    name
    email
  }
}
```

Click the "Play" button and see the results!

## 📊 GraphQL Schema

### Types

#### User
```graphql
type User {
  id: Int!
  username: String!
  email: String!
  name: String!
  age: Int!
  city: String!
  createdAt: String!
  posts: [Post!]!           # User's posts
  comments: [Comment!]!     # User's comments
  postCount: Int!           # Computed field
}
```

#### Post
```graphql
type Post {
  id: Int!
  title: String!
  content: String!
  authorId: Int!
  published: Boolean!
  createdAt: String!
  likes: Int!
  author: User              # Post author
  comments: [Comment!]!     # Post comments
  commentCount: Int!        # Computed field
  excerpt(length: Int): String!  # Field with argument
}
```

#### Comment
```graphql
type Comment {
  id: Int!
  text: String!
  authorId: Int!
  postId: Int!
  createdAt: String!
  author: User              # Comment author
  post: Post                # Related post
}
```

### Queries

```graphql
type Query {
  hello: String!
  user(id: Int!): User
  users(limit: Int): [User!]!
  post(id: Int!): Post
  posts(publishedOnly: Boolean): [Post!]!
  searchPosts(keyword: String!): [Post!]!
  popularPosts(minLikes: Int): [Post!]!
}
```

### Mutations

```graphql
type Mutation {
  createUser(input: CreateUserInput!): User!
  createPost(input: CreatePostInput!): Post!
  createComment(input: CreateCommentInput!): Comment!
  updatePost(input: UpdatePostInput!): Post
  deletePost(postId: Int!): Boolean!
}
```

## 📝 Example Queries

### 1. Simple Query

```graphql
query {
  hello
}
```

### 2. Get User with Posts

```graphql
query {
  user(id: 1) {
    name
    email
    postCount
    posts {
      title
      likes
    }
  }
}
```

### 3. Get Post with Author and Comments

```graphql
query {
  post(id: 1) {
    title
    content
    author {
      name
      email
    }
    comments {
      text
      author {
        name
      }
    }
  }
}
```

### 4. Search Posts

```graphql
query {
  searchPosts(keyword: "GraphQL") {
    id
    title
    author {
      name
    }
  }
}
```

### 5. Get Popular Posts

```graphql
query {
  popularPosts(minLikes: 50) {
    title
    likes
    commentCount
  }
}
```

### 6. Create a User

```graphql
mutation {
  createUser(input: {
    username: "jane_doe"
    email: "jane@example.com"
    name: "Jane Doe"
    age: 28
    city: "Austin"
  }) {
    id
    name
    email
  }
}
```

### 7. Create a Post

```graphql
mutation {
  createPost(input: {
    title: "My First GraphQL Post"
    content: "Learning GraphQL is fun!"
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
```

### 8. Update a Post

```graphql
mutation {
  updatePost(input: {
    postId: 5
    title: "Updated Title"
    published: true
  }) {
    id
    title
    published
  }
}
```

### 9. Using Variables

**Query:**
```graphql
query GetUser($userId: Int!) {
  user(id: $userId) {
    name
    email
    posts {
      title
    }
  }
}
```

**Variables:**
```json
{
  "userId": 1
}
```

### 10. Multiple Queries (Aliases)

```graphql
query {
  firstUser: user(id: 1) {
    name
    postCount
  }
  secondUser: user(id: 2) {
    name
    postCount
  }
  allUsers: users(limit: 3) {
    name
  }
}
```

## 🔧 Running Client Examples

The project includes a Python client with 14 example queries:

```bash
# Make sure the server is running first
python main.py

# In another terminal, run the examples
python client_examples.py
```

This will execute:
1. Simple query
2. Fetch users
3. User with posts (nested)
4. Post with relationships (deep nesting)
5. Query with variables
6. Field arguments
7. Search posts
8. Popular posts
9. Create user mutation
10. Create post mutation
11. Create comment mutation
12. Update post mutation
13. Multiple operations
14. Aliases

## 📚 API Documentation

### REST Endpoint

The API also provides a REST endpoint for information:

```bash
curl http://localhost:8000/
```

### Health Check

```bash
curl http://localhost:8000/health
```

### FastAPI Docs

FastAPI automatically generates OpenAPI documentation:

```
http://localhost:8000/docs
```

## 🎓 Learning Resources

### Included Documentation

1. **GRAPHQL_EXPLAINED.md** - Comprehensive guide covering:
   - What is GraphQL?
   - How GraphQL works
   - Core concepts (types, queries, mutations)
   - Advantages of GraphQL (10 major benefits)
   - GraphQL vs REST comparison
   - When to use GraphQL
   - Real-world use cases
   - Performance considerations

2. **This README** - Quick start and examples

3. **Code Comments** - Detailed comments in all files

### External Resources

- [GraphQL Official Website](https://graphql.org/)
- [Strawberry GraphQL Docs](https://strawberry.rocks/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [How to GraphQL Tutorial](https://www.howtographql.com/)

## 🎯 Key Concepts Demonstrated

### 1. Type System
- Scalar types (Int, String, Boolean)
- Object types (User, Post, Comment)
- Non-null modifiers (!)
- Lists ([Post!]!)

### 2. Relationships
- One-to-many (User → Posts)
- Many-to-one (Post → User)
- Nested relationships (User → Posts → Comments)

### 3. Resolvers
- Field resolvers for relationships
- Computed fields (postCount, commentCount)
- Field arguments (excerpt length)

### 4. Queries
- Simple queries
- Nested queries
- Queries with arguments
- Queries with variables
- Multiple queries with aliases

### 5. Mutations
- Create operations
- Update operations
- Delete operations
- Input types

## 🔍 Understanding the Code

### Main Components

**main.py**: FastAPI application
- Sets up FastAPI app
- Integrates GraphQL router
- Provides REST endpoints

**schema.py**: GraphQL schema
- Defines all types (User, Post, Comment)
- Defines Query operations
- Defines Mutation operations
- Implements all resolvers

**models.py**: Data layer
- In-memory database simulation
- CRUD operations
- Sample data initialization

**client_examples.py**: Client code
- Python requests examples
- Query execution
- Result formatting

## 🌟 Advantages You'll See

### 1. No Over-fetching
Query only the fields you need:
```graphql
query {
  user(id: 1) {
    name  # Only get name, not all user data
  }
}
```

### 2. No Under-fetching
Get related data in one request:
```graphql
query {
  user(id: 1) {
    name
    posts {      # Get posts in same request
      title
      comments { # Get comments too!
        text
      }
    }
  }
}
```

### 3. Strong Typing
Invalid queries are rejected:
```graphql
query {
  user(id: "invalid") {  # Error: ID must be Int
    name
  }
}
```

### 4. Self-Documentation
Schema introspection reveals API structure automatically.

## 🚦 Next Steps

1. **Explore the Schema**
   - Open GraphQL Playground
   - Click "Docs" to see schema
   - Try different queries

2. **Run Examples**
   - Execute `client_examples.py`
   - Modify queries
   - Create your own

3. **Read the Guide**
   - Open `GRAPHQL_EXPLAINED.md`
   - Understand concepts deeply
   - Learn best practices

4. **Experiment**
   - Add new types
   - Create new queries
   - Implement subscriptions
   - Add database integration

## 🛠️ Customization

### Add a New Type

1. Define in `schema.py`:
```python
@strawberry.type
class Product:
    id: int
    name: str
    price: float
```

2. Add to Query:
```python
@strawberry.field
def product(self, id: int) -> Optional[Product]:
    # Implement resolver
    pass
```

### Add a New Query

```python
@strawberry.field
def search_users(self, city: str) -> List[User]:
    users_data = [u for u in db.users if u["city"] == city]
    return [User(**user) for user in users_data]
```

## 📈 Performance Tips

1. **Use DataLoader** for batching (prevent N+1 queries)
2. **Implement pagination** for large lists
3. **Add query complexity limits**
4. **Use persisted queries** in production
5. **Enable caching** at resolver level

## 🤝 Contributing

Feel free to:
- Add more examples
- Improve documentation
- Report issues
- Suggest features

## 📄 License

This is a demo project for educational purposes.

---

**Happy GraphQL Learning!** 🚀

For detailed explanation of GraphQL concepts and advantages, see [GRAPHQL_EXPLAINED.md](GRAPHQL_EXPLAINED.md)
