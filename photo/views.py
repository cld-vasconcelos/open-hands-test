from django.http import HttpRequest, HttpResponse
from strawberry.django.views import GraphQLView

from photo.queries import Context


class ReventGraphQLView(GraphQLView):
    def get_context(self, request, response: HttpResponse) -> any:
        context = Context()
        context.request = request
        return context

from django.views import View
from django.http import JsonResponse
from photo.models import ContestSubmission
from django.db.models import F

class WinnersView(View):
    def get(self, request):
        winners = ContestSubmission.objects.filter(contest__winners__isnull=False)
        data = winners.annotate(
            contest_title=F('contest__title'),
            contest_description=F('contest__description'),
            contest_end_date=F('contest__voting_phase_end'),
            winner_name=F('picture__user__name_first'),
            winning_photo=F('picture__file')
        ).values(
            'contest_title',
            'contest_description',
            'contest_end_date',
            'winner_name',
            'winning_photo'
        ).order_by('contest_end_date')
        return JsonResponse(list(data), safe=False)
