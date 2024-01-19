from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from .models import Food, Consume
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == "POST":
        food_consumed = request.POST.get("food_consumed") # the food selected in the html template

        # Check if the form has been submitted with a non-empty food_consumed value
        if food_consumed:
            food = Food.objects.get(name=food_consumed)
            user = request.user

            # Check if the food is not already in the session (i.e. saves it so on page refresh doesn't get resubmitted)
            if 'selected_food' not in request.session or food.name != request.session['selected_food']:
                consume = Consume(user=user, food_consumed=food)
                consume.save()

                # Store the selected food in the session
                request.session['selected_food'] = food.name
                request.session.save()

                # Show a success message for adding the item
                messages.success(request, f"Item '{food.name}' added successfully!")

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)

    context = {
        "foods": foods,
        "consumed_food": consumed_food,
    }

    return render(request, 'myapp/index.html', context)


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    
    if request.method == "POST":
        food_name = consumed_food.food_consumed.name
        consumed_food.delete()

        messages.success(request, f"Item '{food_name}' removed successfully!")
        return redirect('/') # redirecting to homepage
    
    return redirect('/') 
