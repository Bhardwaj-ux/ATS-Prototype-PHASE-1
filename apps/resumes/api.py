from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import ResumeFile


class ResumeListAPIView(LoginRequiredMixin, View):
    def get(self, request):
        resumes = list(
            ResumeFile.objects.select_related('application', 'application__job')
            .order_by('-created_at')
            .values(
                'id',
                'original_filename',
                'file_size',
                'mime_type',
                'created_at',
                'application__full_name',
                'application__job__title',
            )
        )
        return JsonResponse({'resumes': resumes})
