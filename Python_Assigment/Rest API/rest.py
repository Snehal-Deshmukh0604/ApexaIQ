"""
Simple REST API Client - JSONPlaceholder
"""

import requests

def get_users():
    """Get all users from API"""
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()  # Raises exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users: {e}")
        return None

def get_user_posts(user_id):
    """Get posts by specific user"""
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")
        return None

def create_post(title, body, user_id):
    """Create a new post"""
    try:
        data = {
            'title': title,
            'body': body,
            'userId': user_id
        }
        response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating post: {e}")
        return None

# Demo the API client
if __name__ == "__main__":
    print("=== REST API CLIENT DEMO ===")
    print()
    
    # 1. Get all users
    print("1. FETCHING USERS:")
    users = get_users()
    if users:
        for user in users[:3]:  # Show first 3 users
            print(f"   - {user['name']} | {user['email']}")
    
    # 2. Get posts for user 1
    print("\n2. FETCHING POSTS FOR USER 1:")
    posts = get_user_posts(1)
    if posts:
        for post in posts[:2]:  # Show first 2 posts
            print(f"   - {post['title']}")
    
    # 3. Create a new post
    print("\n3. CREATING NEW POST:")
    new_post = create_post(
        "My Test Post", 
        "This is a test post created via Python API client", 
        1
    )
    if new_post:
        print("   SUCCESS! Post created successfully!")
        print(f"   Post ID: {new_post['id']}")
        print(f"   Title: {new_post['title']}")