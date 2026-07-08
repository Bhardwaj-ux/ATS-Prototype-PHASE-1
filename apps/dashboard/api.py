from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.views import View

from apps.applications.models import Application
from apps.jobs.models import Job
from apps.resumes.models import ResumeFile


class DashboardStatsAPIView(LoginRequiredMixin, View):
    def get(self, request):
        job_count = Job.objects.filter(is_active=True).count()
        application_count = Application.objects.count()
        resume_count = ResumeFile.objects.count()
        status_breakdown = list(
            Application.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )
        latest_applications = list(
            Application.objects.select_related("job")
            .order_by("-created_at")[:10]
            .values(
                "id",
                "full_name",
                "email",
                "status",
                "created_at",
                "job__title",
            )
        )

        return JsonResponse(
            {
                "brand": "Elecbits ATS",
                "job_count": job_count,
                "application_count": application_count,
                "resume_count": resume_count,
                "status_breakdown": status_breakdown,
                "latest_applications": [
                    {
                        "id": item["id"],
                        "full_name": item["full_name"],
                        "email": item["email"],
                        "status": item["status"],
                        "created_at": item["created_at"].isoformat(),
                        "job_title": item["job__title"],
                    }
                    for item in latest_applications
                ],
            }
        )
