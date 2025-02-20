from django import forms
from .models import MCQ


class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQ
        fields = ['subject', 'difficulty', 'question_text', 'question_image',
                  'option_a', 'option_a_image', 'option_b', 'option_b_image',
                  'option_c', 'option_c_image', 'option_d', 'option_d_image',
                  'correct_answer', 'tags']
