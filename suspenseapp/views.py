from django.shortcuts import render

from .models import Suspense

from .forms import SearchSuspenseForm, EmpSearchSuspenseForm, NsfSearchSuspenseForm


# Create your views here.
def suspensesearch(request):

    # Initialize form for searching members
    search_form = SearchSuspenseForm(request.GET or None)
    results = []
    if request.method == "GET":
        if search_form.is_valid():
            query = search_form.cleaned_data['q']
            results = Suspense.objects.filter(member_name__icontains=query)

    return render(request, 'member_suspensesearch.html', {'search_form': search_form, 'results': results})


# Create your views here.
def empl_suspensesearch(request):

    # Initialize form for searching members
    search_form = EmpSearchSuspenseForm(request.GET or None)
    results = []
    if request.method == "GET":
        if search_form.is_valid():
            query = search_form.cleaned_data['q']
            results = Suspense.objects.filter(employer_name__icontains=query)

    return render(request, 'employer_suspensesearch.html', {'search_form': search_form, 'results': results})

# Create your views here.
def nsf_suspensesearch(request):

    # Initialize form for searching members
    search_form = NsfSearchSuspenseForm(request.GET or None)
    results = []
    if request.method == "GET":
        if search_form.is_valid():
            query = search_form.cleaned_data['q']
            results = Suspense.objects.filter(employerno__icontains=query)

    return render(request, 'nsf_suspensesearch.html', {'search_form': search_form, 'results': results})


