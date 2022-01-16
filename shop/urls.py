from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('loguser', views.login_user, name='loguser'),
    path('login',views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup',views.signup, name='signup'),
    path('home',views.home, name='home'),
    path('catelog', views.catelog_view, name='catelog'),
    path('search', views.search, name='search'),
    path('developer', views.developer_view, name='developer'),
    path('games/<int:game_id>/play', views.play_game, name='play_game'),
    path('developer/publish', views.publish_page_view, name='publish'),
    path('developer/mygames', views.developer_games, name='developer_games'),
    path('developer/games/<int:game_id>/edit', views.edit_game, name='editgame'),
    path('developer/publish_game', views.create_game, name='developer_games'),


]