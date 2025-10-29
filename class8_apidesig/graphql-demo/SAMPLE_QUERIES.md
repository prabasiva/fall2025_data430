# GraphQL Sample Queries Collection

Copy and paste these queries into the GraphQL Playground at `http://localhost:8000/graphql`

## Basic Queries

### 1. Hello World
```graphql
query {
  hello
}
```

### 2. Get All Users
```graphql
query {
  users {
    id
    name
    email
    city
  }
}
```

### 3. Get Limited Users
```graphql
query {
  users(limit: 3) {
    id
    name
    email
  }
}
```

### 4. Get Single User
```graphql
query {
  user(id: 1) {
    id
    username
    name
    email
    age
    city
    createdAt
  }
}
```

### 5. Get All Posts
```graphql
query {
  posts {
    id
    title
    content
    likes
    published
    createdAt
  }
}
```

### 6. Get Only Published Posts
```graphql
query {
  posts(publishedOnly: true) {
    id
    title
    likes
  }
}
```

## Nested Queries (Relationships)

### 7. User with Their Posts
```graphql
query {
  user(id: 1) {
    name
    email
    posts {
      id
      title
      likes
      published
    }
  }
}
```

### 8. User with Posts and Comments
```graphql
query {
  user(id: 1) {
    name
    email
    postCount
    posts {
      title
      commentCount
      comments {
        text
      }
    }
  }
}
```

### 9. Post with Author
```graphql
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
      city
    }
  }
}
```

### 10. Post with Author and Comments
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
      createdAt
      author {
        name
      }
    }
  }
}
```

### 11. Deep Nesting - Post → Comments → Author → Posts
```graphql
query {
  post(id: 1) {
    title
    comments {
      text
      author {
        name
        posts {
          title
        }
      }
    }
  }
}
```

## Computed Fields

### 12. User Post Count
```graphql
query {
  users {
    name
    postCount
  }
}
```

### 13. Post Comment Count
```graphql
query {
  posts(publishedOnly: true) {
    title
    likes
    commentCount
  }
}
```

### 14. Post Excerpt (Field with Argument)
```graphql
query {
  posts {
    title
    excerpt(length: 50)
    likes
  }
}
```

### 15. Different Excerpt Lengths
```graphql
query {
  post(id: 1) {
    title
    shortExcerpt: excerpt(length: 30)
    longExcerpt: excerpt(length: 100)
  }
}
```

## Advanced Queries

### 16. Search Posts by Keyword
```graphql
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
```

### 17. Get Popular Posts
```graphql
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
```

### 18. Multiple Queries with Aliases
```graphql
query {
  alice: user(id: 1) {
    name
    postCount
  }
  bob: user(id: 2) {
    name
    postCount
  }
  publishedPosts: posts(publishedOnly: true) {
    title
  }
  allPosts: posts {
    title
  }
}
```

### 19. Query with Variables
```graphql
query GetUser($userId: Int!) {
  user(id: $userId) {
    name
    email
    posts {
      title
      likes
    }
  }
}

# Variables (in separate panel):
{
  "userId": 1
}
```

### 20. Query with Multiple Variables
```graphql
query GetPostsAndUser($userId: Int!, $minLikes: Int!) {
  user(id: $userId) {
    name
    posts {
      title
      likes
    }
  }
  popularPosts(minLikes: $minLikes) {
    title
    likes
    author {
      name
    }
  }
}

# Variables:
{
  "userId": 1,
  "minLikes": 50
}
```

## Mutations

### 21. Create User
```graphql
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
    createdAt
  }
}
```

### 22. Create Post
```graphql
mutation {
  createPost(input: {
    title: "My First GraphQL Post"
    content: "Learning GraphQL is exciting! It provides so much flexibility."
    authorId: 1
    published: true
  }) {
    id
    title
    content
    author {
      name
    }
    createdAt
  }
}
```

### 23. Create Draft Post
```graphql
mutation {
  createPost(input: {
    title: "Draft Post"
    content: "This is a draft that will be published later."
    authorId: 1
    published: false
  }) {
    id
    title
    published
  }
}
```

### 24. Create Comment
```graphql
mutation {
  createComment(input: {
    text: "Great post! Very informative."
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
    createdAt
  }
}
```

### 25. Update Post
```graphql
mutation {
  updatePost(input: {
    postId: 5
    title: "Updated: Upcoming Features"
    published: true
  }) {
    id
    title
    published
    content
  }
}
```

### 26. Update Post Content Only
```graphql
mutation {
  updatePost(input: {
    postId: 2
    content: "Updated content here..."
  }) {
    id
    title
    content
  }
}
```

### 27. Delete Post
```graphql
mutation {
  deletePost(postId: 5)
}
```

### 28. Mutation with Named Operation
```graphql
mutation CreateNewUser {
  createUser(input: {
    username: "jane_smith"
    email: "jane@example.com"
    name: "Jane Smith"
    age: 25
    city: "Seattle"
  }) {
    id
    name
  }
}
```

### 29. Mutation with Variables
```graphql
mutation CreatePost($title: String!, $content: String!, $authorId: Int!) {
  createPost(input: {
    title: $title
    content: $content
    authorId: $authorId
    published: true
  }) {
    id
    title
    author {
      name
    }
  }
}

# Variables:
{
  "title": "Variable Test Post",
  "content": "This post was created using variables",
  "authorId": 1
}
```

## Complex Scenarios

### 30. Get Complete User Profile
```graphql
query UserProfile($userId: Int!) {
  user(id: $userId) {
    # Basic info
    id
    username
    name
    email
    age
    city
    createdAt

    # Stats
    postCount

    # Posts with details
    posts {
      id
      title
      excerpt(length: 100)
      likes
      published
      commentCount
      createdAt
    }

    # Comments made by user
    comments {
      text
      createdAt
      post {
        title
        author {
          name
        }
      }
    }
  }
}

# Variables:
{
  "userId": 1
}
```

### 31. Dashboard Query
```graphql
query Dashboard {
  # Total users
  allUsers: users {
    id
    name
  }

  # Recent published posts
  recentPosts: posts(publishedOnly: true) {
    id
    title
    likes
    commentCount
    createdAt
    author {
      name
    }
  }

  # Popular posts
  topPosts: popularPosts(minLikes: 40) {
    title
    likes
    author {
      name
    }
  }
}
```

### 32. Search and Filter
```graphql
query SearchAndFilter($keyword: String!, $minLikes: Int!) {
  searchResults: searchPosts(keyword: $keyword) {
    id
    title
    excerpt(length: 80)
    likes
    author {
      name
    }
  }

  popularResults: popularPosts(minLikes: $minLikes) {
    id
    title
    likes
  }
}

# Variables:
{
  "keyword": "API",
  "minLikes": 30
}
```

### 33. Batch Create Workflow
```graphql
mutation CreateUserAndPost {
  # First, create a user
  newUser: createUser(input: {
    username: "batch_user"
    email: "batch@example.com"
    name: "Batch User"
    age: 28
    city: "Portland"
  }) {
    id
    name
  }

  # Note: In a real scenario, you'd use the returned ID
  # For demo, we'll use an existing user ID
  newPost: createPost(input: {
    title: "Batch Created Post"
    content: "This demonstrates batch operations"
    authorId: 1
    published: true
  }) {
    id
    title
  }
}
```

## Introspection Queries

### 34. Get Schema Types
```graphql
query {
  __schema {
    types {
      name
      kind
      description
    }
  }
}
```

### 35. Get Query Type Fields
```graphql
query {
  __schema {
    queryType {
      name
      fields {
        name
        description
        type {
          name
          kind
        }
      }
    }
  }
}
```

### 36. Get User Type Details
```graphql
query {
  __type(name: "User") {
    name
    kind
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

## Performance Testing

### 37. Large Nested Query (Test Performance)
```graphql
query {
  users {
    name
    posts {
      title
      comments {
        text
        author {
          name
          posts {
            title
          }
        }
      }
    }
  }
}
```

### 38. Selective Fields (Optimized)
```graphql
query {
  users {
    name
    postCount  # Computed field, no need to fetch all posts
  }
}
```

## Error Handling Examples

### 39. Query Non-existent User
```graphql
query {
  user(id: 999) {
    name
    email
  }
}
# Returns null for user
```

### 40. Invalid Field (Will Error)
```graphql
query {
  user(id: 1) {
    name
    invalidField  # This will cause a validation error
  }
}
```

## Tips for Using These Queries

1. **Copy and Paste**: Copy any query into GraphQL Playground
2. **Modify**: Change IDs, parameters, and fields to experiment
3. **Variables**: Use the Variables panel for parameterized queries
4. **Documentation**: Click "Docs" in Playground to explore schema
5. **Autocomplete**: Use Ctrl+Space for field suggestions
6. **Format**: Use Prettier (Ctrl+Shift+F) to format queries

## Next Steps

1. Try combining different queries
2. Create your own queries
3. Test mutations and verify results
4. Explore deeply nested relationships
5. Practice with variables
6. Build complex dashboard queries

Happy querying! 🚀
