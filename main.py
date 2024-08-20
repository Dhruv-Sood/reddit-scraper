import praw
import requests
import os

reddit = praw.Reddit(client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="postdownloader")

def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {path}")
    else:
        print(f"Failed to download {url}")

def main():
    subreddit_name = input("Enter the subreddit: ")
    num_photos = int(input("Enter the number of photos to download: "))
    
    directory = f"image/{subreddit_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    subreddit = reddit.subreddit(subreddit_name)
    
    count = 0
    for post in subreddit.top(limit=1000):  # Fetch a large number of posts to increase chances of finding enough images
        if post.url.endswith(('jpg', 'jpeg', 'png')):
            count += 1
            image_name = f"{directory}/{subreddit_name}_{count}.jpg"
            download_image(post.url, image_name)
        if count >= num_photos:
            break

    print(f"Downloaded {count} images from r/{subreddit_name}")

if __name__ == "__main__":
    main()
