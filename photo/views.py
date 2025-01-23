from django.http import HttpRequest, HttpResponse
from strawberry.django.views import GraphQLView
from django.http import JsonResponse
from .models import Contest, ContestSubmission


from photo.queries import Context


class ReventGraphQLView(GraphQLView):
    def get_context(self, request, response: HttpResponse) -> any:
        context = Context()
        context.request = request
        return context
def winners_view(request: HttpRequest) -> JsonResponse:
    contests = Contest.objects.filter(internal_status='CLOSED').order_by('-voting_phase_end')
    winners_data = []
    for contest in contests:
        winner_submission = ContestSubmission.objects.filter(contest=contest, picture__user__in=contest.winners.all()).first()
        if winner_submission:
            winners_data.append({
                'contest_title': contest.title,
                'contest_description': contest.description,
                'contest_ended': contest.voting_phase_end,
                'winner_name': winner_submission.picture.user.name_first + ' ' + winner_submission.picture.user.name_last,
                'winning_photo': winner_submission.picture.file.url
            })
    return JsonResponse(winners_data, safe=False)

                context.request = request
                return context
