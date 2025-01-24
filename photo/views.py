from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F
from django.db.models.functions import Lower

@api_view(['GET'])
def contest_winners(request):
    winners = Contest.objects.annotate(
        winner_name=F('winner__user__username'),
        winning_photo_url=F('winner__image')
    ).values(
        'title', 'description', 'end_date', 'winner_name', 'winning_photo_url'
    ).order_by('end_date')
    return JsonResponse({'winners': list(winners)})
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
