from django.contrib import admin
from .models import *

# @admin.register(BaseAd)
# class AdAdmin(admin.ModelAdmin):
#     list_display = ('title', 'company', 'category', 'created_at')
#     search_fields = ('title', 'description')


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1


class AdAnswerInline(admin.TabularInline):
    model = AdAnswer
    extra = 3
    fields = ('answer_text', 'is_correct')


@admin.register(AdQuestion)
class AdQuestionAdmin(admin.ModelAdmin):
    list_display = ('ad', 'question_text', 'created_at')
    search_fields = ('question_text',)
    inlines = [AdAnswerInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for answer_form in formsets[0].forms:
            if answer_form.cleaned_data.get('is_correct'):
                form.instance.correct_answer = answer_form.instance
                form.instance.save()
                break


@admin.register(AdAnswer)
class AdAnswerAdmin(admin.ModelAdmin):
    list_display = ('question',  'answer_text', 'is_correct', 'created_at')
    search_fields = ('answer_text',)



@admin.register(UserAdHistory)
class UserAdHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'action_type', 'timestamp')
    search_fields = ('user__username', 'ad__title')


@admin.register(BaseAd)
class BaseAdAdmin(admin.ModelAdmin):
    inlines = [AdImageInline]
    list_display = ('title', 'company', 'created_at')
    search_fields = ('title', 'description')