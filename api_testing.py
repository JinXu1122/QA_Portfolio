import requests

# The "Base URL" of the API we are testing
BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_user_posts():
    print("\n--- Running Test: Get User Posts ---")
    
    # 1. SEND REQUEST: The 'waiter' goes to the kitchen (server)
    # We are asking for posts belonging to User #1
    response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})

    # 2. VERIFY STATUS CODE: 200 means "OK/Success"
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200

    # 3. VERIFY DATA: Check if we got the right information
    posts = response.json()
    print(f"Number of posts found: {len(posts)}")
    
    # Assert that the list is not empty and the first post belongs to User 1
    assert len(posts) > 0
    assert posts[0]["userId"] == 1
    print("Test Passed: Successfully retrieved user posts!")

def test_create_new_post():
    print("\n--- Running Test: Create New Post ---")
    
    # New data we want to send to the server
    new_post = {
        "title": "My QA Portfolio Post",
        "body": "This is testing the backend logic.",
        "userId": 1
    }

    # 1. SEND REQUEST: We use 'POST' to send new data to the server
    response = requests.post(f"{BASE_URL}/posts", json=new_post)

    # 2. VERIFY STATUS CODE: 201 means "Created Successfully"
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 201

    # 3. VERIFY DATA: The API usually sends back the object we just created
    created_post = response.json()
    assert created_post["title"] == "My QA Portfolio Post"
    print(f"Test Passed: Post created with ID {created_post['id']}")

if __name__ == "__main__":
    # We can run these manually with 'python api_testing.py'
    # or with 'pytest api_testing.py'
    test_get_user_posts()
    test_create_new_post()