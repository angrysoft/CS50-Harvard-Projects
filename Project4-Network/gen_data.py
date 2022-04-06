from random import randint
from network.models import Post, User
import requests

usernames = [
    "angel",
    "shimmer",
    "angelic",
    "bubbly",
]

for username in usernames:
    user = User.objects.create_user(username, f'{username}@bar.net', '1234')
    user.save()

for no in range(100):
    r = requests.get(
        "https://baconipsum.com/api/?type=meat-and-filler&paras=1&format=text"
    )
    post = Post()
    post.content = r.text
    post.user = User.objects.get(username__exact=(usernames[randint(0, len(usernames)-1)]))
    post.save()
    print(f"added Post no : {no}")
