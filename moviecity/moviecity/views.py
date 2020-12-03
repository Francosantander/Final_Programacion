from django.shortcuts import render
# from django.template import Template, Context
from django.template.loader import get_template


def principal(request):
    return render(request, "principal.html")


def butacas(request):
    return render(request, "no.html")
