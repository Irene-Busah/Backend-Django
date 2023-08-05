from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm
# from django.http import HttpResponse

# Create your views here.
def home_page(request):
    users = User.objects.filter(hackathon_participant=True)
    events = Event.objects.all()
    context = {'users':users, 'events':events}
    return render(request, 'home.html', context=context)

def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context=context)

def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context=context)

def event_page(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'event.html', context=context)

def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    
    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)
    return render(request, 'event_confirmation.html', context=context)

def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect('user-account')
    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context=context)


# https://www.youtube.com/watch?v=531EHxr88LE