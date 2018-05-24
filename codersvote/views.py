"""from django.http import Http404
from django.shortcuts import get_object_or_404,render
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
#
from django.http import HttpResponse
#from django.template import loader

from .models import Question

def index(request):
	latest_question_list=Question.objects.order_by('-pub_date')[:5]
	#output=', '.join([q.question_text for q in latest_question_list])
	template=loader.get_template('codersvote/index.html')
	context={
		'latest_question_list': latest_question_list,
	}
	#return HttpResponse(output)
	#return HttpResponse(template.render(context,request))
	return render(request,'codersvote/index.html',context)

def detail(request, question_id):
	#try:
	#	question=Question.objects.grt(pk=question_id)
	#except Question.DoesNotExist:
	#	raise Http404("Question does not exist")
	#return HttpResponse("You're looking at question %s." %question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'codersvote/detail.html', {'question': question})

def results(request,question_id):
	#response="You're looking at the results of question %s."
	#return HttpResponse(response % question_id)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'codersvote/results.html', {'question': question})

#def  vote(request, question_id):
#	return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'codersvote/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('codersvote:results', args=(question.id,)))
        """
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'codersvote/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.(not including those set to be
    published in the future)."""
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'codersvote/detail.html'
    def get_queryset(self):
    	"""
    	Excludes any questions that aren't published yet.
    	"""
    	return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'codersvote/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'codersvote/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
    	selected_choice.votes+=1
    	selected_choice.save()
    	return HttpResponseRedirect(reverse('codersvote:results',args=(question.id,)))
