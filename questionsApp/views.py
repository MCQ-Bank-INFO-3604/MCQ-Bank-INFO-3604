from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MCQ, Assessment
from .forms import MCQForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



@login_required
def create_mcq(request):
    if request.method == 'POST':
        form = MCQForm(request.POST, request.FILES)
        if form.is_valid():
            mcq = form.save(commit=False)
            mcq.created_by = request.user
            mcq.save()
            return redirect('mcq_list')
    else:
        form = MCQForm()
    return render(request, 'mcq_form.html', {'form': form})
