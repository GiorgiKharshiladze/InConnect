from django.shortcuts import render

# Create your views here.
def api(request):
	return render(request, "index.html")