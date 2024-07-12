from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Cart, CartItem, Order
from django.contrib.auth import authenticate, login, logout
from .forms import ItemForm, CustomerSignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


def signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = CustomerSignUpForm()
    return render(request, "shop/auth/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("landing_page")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "shop/auth/login.html")


def landing_page(request):
    items = Item.objects.all()
    return render(request, "shop/landing_page.html", {"items": items})


def user_logout(request):
    logout(request)
    return redirect("landing_page")


@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, "shop/item_list.html", {"items": items})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, "shop/item_detail.html", {"item": item})


@staff_member_required
@login_required
def item_new(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm()
    return render(request, "shop/item_edit.html", {"form": form})


@staff_member_required
@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, "shop/item_edit.html", {"form": form})


@staff_member_required
@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "shop/item_confirm_delete.html", {"item": item})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.stock <= 0:
        messages.error(request, "This item is sold out.")
        return redirect("item_detail", pk=item_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > item.stock:
        messages.error(request, "Not enough stock available.")
        return redirect("item_detail", pk=item_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        if cart_item.quantity + quantity > item.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("item_detail", pk=item_id)
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, f"{quantity} x {item.name} added to cart.")
    return redirect("item_detail", pk=item_id)


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart.cartitem_set.all())
    return render(request, "shop/cart.html", {"cart": cart, "total": total})


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart.cartitem_set.all())
    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=total)
        for cart_item in cart.cartitem_set.all():
            cart_item.item.stock -= cart_item.quantity
            cart_item.item.save()
            order.items.add(cart_item)
        cart.cartitem_set.all().delete()
        messages.success(request, "Order placed successfully.")
        return redirect("order_receipt", order_id=order.id)
    return render(request, "shop/checkout.html", {"cart": cart, "total": total})


@login_required
def order_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_receipt.html", {"order": order})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.item.name} removed from cart.")
    return redirect("view_cart")


@staff_member_required
def users_page(request):
    users = User.objects.all()
    return render(request, "shop/users_page.html", {"users": users})
