from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# landing pages urls
urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("items/", views.item_list, name="item_list"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),
    path("item/new/", views.item_new, name="item_new"),
    path("item/<int:pk>/edit/", views.item_edit, name="item_edit"),
    path("item/<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("add_to_cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order_receipt/<int:order_id>/", views.order_receipt, name="order_receipt"),
    path(
        "remove_from_cart/<int:cart_item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("users/", views.users_page, name="users_page"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
