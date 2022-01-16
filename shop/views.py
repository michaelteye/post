from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_list_or_404
from django.http import HttpResponse
from shop.models import Developer, Game, Player, Transaction
from django.contrib.auth.models import User, Group
# Create your views here.
def index(request):
    if request.method == 'GET':
        user = request.user
        if not request.user.is_authenticated:
            return redirect("shop:home")
        if user.groups.filter(name="developers").count() != 0:
            return redirect("shop:developer")
        transactions = Transaction.objects.filter(player=user.player.id)
        purchase_games = []
        for transaction in transactions:
            purchase_games.append(transaction.game)
        return render(request, "shop/index.html", {"user":user, "purchased_game":purchase_games })

def signup(request):
    if request.user.is_authenticated:
        return redirect("shop:index")
    return render(request, 'shop/signup.html')


def logout_view(request):
    logout(request)
    return redirect("shop:login")



def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    return render(request, 'shop/login.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            return render(request, 'shop/login.html', {"error":"One of the field was empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop:index")
        else:
            return render(request, "shop/login.html", {"error":"please provide login details"})
    else:
        return redirect("shop:index")

def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("shop:index")
        games = Game.objects.all()
        return render(request, "shop/home.html", {"games":games})

    else:
        return HttpResponse(status =500)


def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        developer = False
        try:
            if request.POST['developer']:
                developer = True
        except KeyError:
            developer = False
        if username is not None and email is not None and password is not None:
            if not username or not password:
                return render(request, "shop/signup.html", {"error":"Please fill in all required fields"})
            
            if User.objects.filter(username=username).exists():
                return render(request, "shop/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "shop/signup.html",{"error": "email already exists"})

            user = User.objects.create_user(username, email, password)

            if developer:
                if Group.objects.filter(name="developers").exists():
                    dev_group = Group.objects.get(name = "developers")
                else:
                    Group.objects.create(name = 'developers').save()
                    dev_group = Group.objects.get(name = 'developers')
                dev_group.user_set.add(user)
                Developer.objects.create(user=user).save()
            else:
                Player.objects.create(user=user).save()

            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("shop:index")
    else:
        return redirect("shop:signup")

def catelog_view(request):
    pass

def play_game(request, game_id):
    pass

def developer_view(request):
    if request.method == "GET":
        user = request.user
    if not user.is_authenticated:
        return redirect("shop:login")

    if user.groups.filter(name= "developers").count() != 0:
        games = Game.objects.filter(developer=user.developer.id)
        statistics = []
        for game in games:
            transactions = Transaction.objects.filter(game= game.id)
            for transaction in transactions:
                statistics.append(transaction)
            return render(request, "shop/developer.html", {"statistics":statistics})
        else:
            return redirect("shop:index")

def search(request):
    pass

def publish_page_view(request):
      if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop: login")
        if user.groups.filter(name= "developers").count() !=0:
        
            return render(request, "shop/publish_game_form.html")
        
        else:
            return redirect("shop:index")

def developer_games(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop: login")
        if user.groups.filter(name= "developers").count() !=0:
            games = user.developer.game_set.all()
            return render(request, "shop/developer_games.html", {"games":games})
        
        else:
            return redirect("shop:index")

def edit_game(request, game_id):
    pass

def create_game(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status = 500)
        if user.groups.filter(name= "developers").count() == 0:
            return HttpResponse(status = 500)
        developer = user.developer
        title = request.POST['  title']
        price = request.POST['price']
        url = request.POST['url']

        if not title and not url and not price:
            return render(request, "shop/publish_game_form", {"error":"Please fill in all requirement"})

        try:
            float_price = float(price)
        except ValueError:
            return render(request, "shop/pulish_game_form", {"error": "Price is not a number"})

        if float_price <= 0:
            return render(request, "shop/publish_game_form", {"error":"price must be more than 1"})

        try:
            URLValidator()(url)
        
        except ValidationError:
            return render(request, "shop/publish_game_form", {"error":"URL is not valid"})

