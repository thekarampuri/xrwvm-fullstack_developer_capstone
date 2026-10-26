import json
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = {}
    if request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            try:
                data = json.loads(request.body)
            except Exception:
                data = request.POST
    else:
        data = request.POST

    username = data.get('userName', data.get('username', ''))
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    res_data = {"userName": username}
    if user is not None:
        login(request, user)
        res_data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(res_data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = {}
    if request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            try:
                data = json.loads(request.body)
            except Exception:
                data = request.POST
    else:
        data = request.POST

    username = data.get('userName', data.get('username', ''))
    password = data.get('password', '')
    first_name = data.get('firstName', data.get('first_name', ''))
    last_name = data.get('lastName', data.get('last_name', ''))
    email = data.get('email', '')
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug(f"{username} is new user")

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        res_data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(res_data)
    else:
        res_data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(res_data)


# Get list of cars (makes and models)
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` view to render the dealerships
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews is not None:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                print(response)
                if response and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = "neutral"
        else:
            reviews = []
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create an `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        data = {}
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except Exception:
                try:
                    data = json.loads(request.body)
                except Exception:
                    data = request.POST
        else:
            data = request.POST
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            logger.error(f"Error posting review: {err}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 400, "message": "Invalid request method"})
