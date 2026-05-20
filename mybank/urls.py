from django.contrib import admin
from django.urls import path

from bank import views
from accounts import views as accounts_views


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.dashboard_view, name='dashboard'),

    path('add-money/', views.add_money, name='add_money'),

    path('transfer/', views.transfer_view, name='transfer'),

    path('history/', views.transaction_history, name='history'),

    # auth
    path('signup/', accounts_views.sign_up, name='sign_up'),

    path('login/', accounts_views.login_view, name='login'),

    path('logout/', accounts_views.logout_view, name='logout'),

]