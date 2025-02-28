# customization/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WorkoutForm
from .models import Routine, Workout
from django.http import HttpResponse

@login_required
def customize_routine_view(request):
    routines = Routine.objects.filter(user=request.user)

    # Create a new routine if the user doesn't have any
    if not routines.exists():
        routine = Routine.objects.create(user=request.user)
    else:
        routine = routines.first()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)

        # Add more workout
        if 'add_more_workout' in request.POST:
            if form.is_valid():
                order = routine.workout_set.count() + 1
                workout = form.save(commit=False)
                workout.routine = routine
                workout.order = order
                workout.save()

        # Remove workout
        elif 'remove_workout' in request.POST:
            workout_id = request.POST['remove_workout']
            workout = get_object_or_404(Workout, id=workout_id, routine=routine)
            workout.delete()

        # Save routine
        elif 'save_routine' in request.POST:
            return redirect('customize_routine')  # Redirect to refresh the page after submission

        # Let's Workout button
        elif 'lets_workout' in request.POST:
            # Redirect to the first workout in the routine
            first_workout = routine.workout_set.order_by('order').first()
            if first_workout:
                return redirect('workout_redirect', exercise_name=first_workout.exercise,
                                rep_count=first_workout.rep_count, time_limit=first_workout.time_limit_seconds)
            else:
                # Handle the case where there are no workouts in the routine
                return HttpResponse("No workouts in the routine.")

    else:
        form = WorkoutForm()

    workouts = routine.workout_set.all()

    return render(request, 'customization/customize_routine.html', {'form': form, 'workouts': workouts})


# customization/views.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Routine, Workout

@login_required
def workout_redirect_view(request, exercise_name, rep_count, time_limit):
    # Logic to determine the redirect URL based on the exercise name
    if exercise_name == 'squats':
        # Example URL for squats app
        return redirect(f'/squats?rep_count={rep_count}&time_limit={time_limit}')
    elif exercise_name == 'bicep_curls':
        # Example URL for bicep_curls app
        return redirect(f'/bicep_curls?rep_count={rep_count}&time_limit={time_limit}')
    else:
        # Add more cases for other exercises if needed
        return redirect('/')

# Add this view to your urlpatterns in customization/urls.py
