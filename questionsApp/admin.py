from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import User, MCQ, Assessment


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


# MCQ Admin
class MCQAdmin(admin.ModelAdmin):
    list_display = ('subject', 'difficulty', 'question_text', 'created_by', 'created_at', 'question_image_preview')
    search_fields = ('subject', 'question_text', 'tags')
    list_filter = ('difficulty', 'created_at', 'subject')

    def question_image_preview(self, obj):
        if obj.question_image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.question_image.url)
        return "No Image"

    question_image_preview.short_description = 'Question Image'



# Function to generate PDF
def generate_assessment_pdf(assessment):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{assessment.title}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, f"Assessment: {assessment.title}")

    # Lecturer Name
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Lecturer: {assessment.lecturer.username}")

    # Line Separator
    p.line(100, height - 90, width - 100, height - 90)

    # List MCQs
    y_position = height - 120
    for index, mcq in enumerate(assessment.mcqs.all(), start=1):
        if y_position < 100:  # Add new page if space runs out
            p.showPage()
            y_position = height - 50

        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y_position, f"{index}. {mcq.question_text}")

        # Options
        p.setFont("Helvetica", 11)
        p.drawString(120, y_position - 20, f"A) {mcq.option_a}")
        p.drawString(120, y_position - 40, f"B) {mcq.option_b}")
        p.drawString(120, y_position - 60, f"C) {mcq.option_c}")
        p.drawString(120, y_position - 80, f"D) {mcq.option_d}")

        y_position -= 100  # Move down for the next question

    # Save PDF
    p.showPage()
    p.save()

    return response


# Custom Admin View
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lecturer', 'created_at', 'generate_pdf_button')
    filter_horizontal = ('mcqs',)

    def generate_pdf_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Generate PDF</a>',
            f'generate_pdf/{obj.id}/'
        )
    generate_pdf_button.short_description = "Generate PDF"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate_pdf/<int:assessment_id>/', self.admin_site.admin_view(self.generate_pdf_view), name="generate_pdf"),
        ]
        return custom_urls + urls

    def generate_pdf_view(self, request, assessment_id):
        assessment = Assessment.objects.get(pk=assessment_id)
        return generate_assessment_pdf(assessment)


# Register Models
admin.site.register(User, CustomUserAdmin)
admin.site.register(MCQ, MCQAdmin)
admin.site.register(Assessment, AssessmentAdmin)
