from django.shortcuts import render

# Create your views here.
def match1(request):
    return render(request, 'match2/match1.html')

def match2(request):
    return render(request, 'match2/match2.html')

def match3(request):
    return render(request, 'match2/match3.html')

def match4(request):
    return render(request, 'match2/match4.html')

def match5(request):
    return render(request, 'match2/match5.html')