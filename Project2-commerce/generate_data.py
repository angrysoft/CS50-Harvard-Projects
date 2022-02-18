from random import randint
from auctions.models import Listing, Category, User
import requests

categories = ("Fashion", "Toys", "Electronics", "Home", "Motorization")
for category_name in categories:
    cat = Category(name=category_name)
    cat.save()

wh = ["200/300", "300/200", "400/400"]


for i in range(15):
    r = requests.get(
        "https://baconipsum.com/api/?type=meat-and-filler&paras=1&format=text"
    )
    img = requests.get(f"https://picsum.photos/{wh[randint(0,2)]}?random=1")
    listing = Listing()
    listing.title = f"Title Foo {i}"
    listing.description = r.text
    listing.image = img.url
    listing.owner = User.objects.get(username__exact="test")
    listing.start_bid = randint(0, 10000)
    listing.save()
    listing.categories.add(
        Category.objects.get(name__exact=categories[randint(0, 4)])
    )
    print(f"Added Title {i}")
