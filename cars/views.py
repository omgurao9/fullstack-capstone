import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Dealer, Review, CarMake, CarModel

def _json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

def _dealer_json(dealer):
    return {
        "id": dealer.id, "name": dealer.name, "city": dealer.city,
        "state": dealer.state, "address": dealer.address, "zip": dealer.zip_code,
        "phone": dealer.phone, "website": dealer.website, "image_url": dealer.image_url,
    }

def _review_json(review):
    return {
        "id": review.id, "dealer_id": review.dealer_id, "name": review.display_name(),
        "review": review.review, "purchase": review.purchase,
        "purchase_date": review.purchase_date.isoformat() if review.purchase_date else None,
        "sentiment": review.sentiment, "created_at": review.created_at.isoformat(),
    }

def _sentiment(text):
    positive = {"fantastic", "great", "excellent", "good", "amazing", "wonderful", "helpful", "friendly", "love", "best", "fast", "perfect"}
    negative = {"bad", "poor", "terrible", "awful", "rude", "slow", "worst", "hate", "disappointing", "unhelpful"}
    words = {w.strip(".,!?;:").lower() for w in text.split()}
    score = len(words & positive) - len(words & negative)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"label": label, "score": score, "text": text}

@ensure_csrf_cookie
def home(request):
    state = request.GET.get("state", "").strip()
    dealers = Dealer.objects.all().order_by("state", "name")
    if state:
        dealers = dealers.filter(state__iexact=state)
    return render(request, "home.html", {"dealers": dealers, "selected_state": state})

def about(request):
    return render(request, "About.html")

def contact(request):
    return render(request, "Contact.html")

def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html", {"next": request.GET.get("next", "/")})

@require_POST
def form_login(request):
    user = authenticate(request, username=request.POST.get("username", ""), password=request.POST.get("password", ""))
    if user is None:
        messages.error(request, "Invalid username or password.")
        return redirect("login")
    login(request, user)
    return redirect(request.POST.get("next") or "/")

def logout_page(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")

def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return render(request, "dealer_detail.html", {"dealer": dealer, "reviews": dealer.reviews.all()})

def review_page(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    if request.method == "POST":
        review_text = request.POST.get("review", "").strip()
        if not review_text:
            messages.error(request, "Please enter a review.")
        elif not request.user.is_authenticated:
            return redirect(f"/login/?next=/review/{dealer_id}/")
        else:
            result = _sentiment(review_text)
            Review.objects.create(
                dealer=dealer, author=request.user, review=review_text,
                purchase=request.POST.get("purchase", "").strip(),
                sentiment=result["label"],
            )
            messages.success(request, "Your review was posted.")
            return redirect("dealer_detail", dealer_id=dealer.id)
    return render(request, "review.html", {"dealer": dealer})

@require_POST
def api_login(request):
    data = _json_body(request)
    if data is None:
        return HttpResponseBadRequest("Invalid JSON")
    user = authenticate(request, username=data.get("username", ""), password=data.get("password", ""))
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)
    login(request, user)
    return JsonResponse({"message": "Login successful", "username": user.username})

@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})

@require_POST
def api_register(request):
    data = _json_body(request)
    if data is None:
        return HttpResponseBadRequest("Invalid JSON")
    required = ["username", "first_name", "last_name", "email", "password"]
    if any(not str(data.get(k, "")).strip() for k in required):
        return JsonResponse({"error": "All five fields are required"}, status=400)
    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already exists"}, status=409)
    user = User.objects.create_user(
        username=data["username"], first_name=data["first_name"],
        last_name=data["last_name"], email=data["email"], password=data["password"]
    )
    return JsonResponse({"message": "Registration successful", "username": user.username}, status=201)

@require_http_methods(["GET"])
def api_dealers(request):
    return JsonResponse({"dealers": [_dealer_json(d) for d in Dealer.objects.all().order_by("id")]})

@require_http_methods(["GET"])
def api_dealers_by_state(request, state):
    dealers = Dealer.objects.filter(state__iexact=state).order_by("id")
    return JsonResponse({"state": state, "dealers": [_dealer_json(d) for d in dealers]})

@require_http_methods(["GET"])
def api_dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    return JsonResponse({"dealer": _dealer_json(dealer)})

@require_http_methods(["GET"])
def api_dealer_reviews(request, dealer_id):
    get_object_or_404(Dealer, pk=dealer_id)
    reviews = Review.objects.filter(dealer_id=dealer_id).select_related("author")
    return JsonResponse({"dealer_id": dealer_id, "reviews": [_review_json(r) for r in reviews]})

@require_http_methods(["GET"])
def api_carmakes(request):
    makes = []
    for make in CarMake.objects.prefetch_related("models").all().order_by("name"):
        makes.append({"id": make.id, "name": make.name, "models": [
            {"id": m.id, "name": m.name, "year": m.year} for m in make.models.all().order_by("year", "name")
        ]})
    return JsonResponse({"car_makes": makes})

@require_POST
def api_analyze_review(request):
    data = _json_body(request)
    if data is None:
        return HttpResponseBadRequest("Invalid JSON")
    text = str(data.get("review", "")).strip()
    if not text:
        return JsonResponse({"error": "review is required"}, status=400)
    return JsonResponse({"sentiment_analysis": _sentiment(text)})
