from django.shortcuts import HttpResponse, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from rezerwacje.models import Auditorium


# base view as fix for csrf
class BaseView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SearchAvaliableAuditoriums(BaseView):

    @csrf_exempt
    def get(self, request):

        auditoriums = Auditorium.objects.all()
        auditoriums_flat = [x for y in [(auditorium.pk, auditorium.name) for auditorium in auditoriums] for x in y]

        form_action = reverse('search-results')

        html_form = """
        <html>
            <body>
                <form action="{form_action}" method="GET">
                    <label>Auditorium capacity
                        <input type="number" min=0 name="capacity">
                    </label><br>
                    <label>Date
                        <input type="date" name="date">
                    </label><br>
                    <label>Projector:<br>
                        <input type="radio" name="projector" value="True">Available<br>
                        <input type="radio" name="projector" value="False">Not available<br>
                    </label><br>
                    <input type="submit" value="Search available auditoriums"/>
                </form>
            </body>
        </html>
        """.format(
            ''.join('<option value="{}">{}</option>' for _ in auditoriums).format(*auditoriums_flat),
                form_action=form_action,
            )
        return HttpResponse(html_form)


class ShowSearchResults(BaseView):

    def get(self, request):

        # build database query using GET params:
        filter_params = dict()
        exclude_params = dict()

        if 'date' in request.GET and request.GET['date'] != '':
            exclude_params['reservations__date'] = request.GET['date']

        if 'capacity' in request.GET and request.GET['capacity'] != '':
            filter_params['capacity__gte'] = request.GET['capacity']

        if 'projector' in request.GET and request.GET['projector'] != '':
            filter_params['projector'] = request.GET['projector']

        auditoriums = Auditorium.objects.exclude(**exclude_params).filter(**filter_params).order_by('capacity')

        if len(auditoriums) == 0:
            return HttpResponse('Brak wolnych sal dla podanych kryteriów wyszukiwania')
        else:
            auditoriums = '<br>'.join('{name}, Capacity: {capacity}. {reservation_link}'.format(
                    name=auditorium.name,
                    capacity=auditorium.capacity,
                    reservation_link='<a href="{}">Reserve</a>'.format(reverse('reserve', kwargs={'id_':auditorium.pk}))
                ) for auditorium in auditoriums)
            return HttpResponse(
                f"""
                Available auditoriums:<br>
                {auditoriums}
                """
            )
