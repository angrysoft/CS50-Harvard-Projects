from network.models import Post, User
import requests


for no in range(30):
    r = requests.get(
        "https://baconipsum.com/api/?type=meat-and-filler&paras=1&format=text"
    )
    post = Post()
    post.content = r.text
    post.user = User.objects.get(username__exact="test")
    post.save()
    print(f"added Post no : {no}")
