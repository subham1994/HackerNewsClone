import datetime
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils.timezone import utc
from .models import Story


# Algorithm to rank the news feed using the votes and the age of the post.

def score(story, gravity=1.8, timebase=120):
    # points variable is raised to a fractional exponent to minimise
    # the impact of votes on the overall score of the story.
    points = (story.points - 1) ** 0.8
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    age = int((now - story.created_at).total_seconds()) / 60

    # age is added to a timebase so that no matter how new the story is,
    # it at least has an age of 2 hrs. it also avoids any 'divide by 0' errors.
    # it has also been raised to a fractional exponent to emphasize its impact on
    # the overall score of the story.
    return points / (age + timebase) ** 1.8


def top_stories(top=180, consider=1000):
    latest_stories = Story.objects.all().order_by('-created_at')[:consider]
    ranked_stories = sorted([(score(story), story) for story in latest_stories], key=lambda story_object: story_object[0], reverse=True)
    return [story for _, story in ranked_stories][:top]


# End of algorithm.


def index(request):
    stories = top_stories(top=35)
    if request.user.is_authenticated():
        liked_stories = request.user.liked_stories.filter(id__in=[story.id for story in stories])
    else:
        liked_stories = []
    context = {'stories': stories, 'user': request.user, 'liked_stories': liked_stories}
    return render_to_response('stories.html', context, context_instance=RequestContext(request))


@login_required
def like(request):
    story = get_object_or_404(Story, id=request.POST.get('story'))
    story.points += 1
    story.save()
    user = request.user
    user.liked_stories.add(story)
    user.save()
    return HttpResponse()
