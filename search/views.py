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

        filter_params = dict()
        exclude_params = dict()

        if 'date' in request.GET and request.GET['date'] != '':
            exclude_params['reservations__date'] = request.GET['date']

        if 'capacity' in request.GET and request.GET['capacity'] != '':
            filter_params['capacity__gte'] = request.GET['capacity']

        if 'projector' in request.GET and request.GET['projector'] != '':
            filter_params['projector'] = request.GET['projector']

        search_parameters = (filter_params.items(), exclude_params.items())
        auditoriums = Auditorium.objects.exclude(**exclude_params).filter(**filter_params)

        if len(auditoriums) == 0:
            return HttpResponse('Brak wolnych sal dla podanych kryteriów wyszukiwania')
        else:
            auditoriums = '<br>'.join(auditorium.name for auditorium in auditoriums)
            return HttpResponse(f'DEBUG: {search_parameters}<br>{auditoriums}')


# old useless code made according to nr.8
# class SearchAvaliableAuditoriumsUseless(BaseView):

#     @csrf_exempt
#     def get(self, request):

#         auditoriums = Auditorium.objects.all()
#         auditoriums_flat = [x for y in [(auditorium.pk, auditorium.name) for auditorium in auditoriums] for x in y]

#         form_action = reverse('search-results')

#         html_form = """
#         <html>
#             <body>
#                 <form action="{form_action}" method="GET">
#                     <fileldset>
#                         <label>Choose Auditorium:
#                             <select name=name required>
#                             {}
#                             </select>
#                         </label>
#                     </fileldset><br>
#                     <label>Auditorium capacity
#                         <input type="number" min=0 step="10" name="capacity" required>
#                     </label><br>
#                     <label>Minimal number of participants
#                         <input type="number" min=0 name="participants" required>
#                     </label><br>
#                     <label>Projector:<br>
#                         <input type="radio" name="projector" value="True" required>Available<br>
#                         <input type="radio" name="projector" value="False" checked>Not available<br>
#                     </label><br>
#                     <input type="submit" value="Search available auditoriums"/>
#                 </form>
#             </body>
#         </html>
#         """.format(
#             ''.join('<option value="{}">{}</option>' for _ in auditoriums).format(*auditoriums_flat),
#                 form_action=form_action,
#             )
#         return HttpResponse(html_form)


# class ShowSearchResults(BaseView):

#     @csrf_exempt
#     def get(self, request):
#         pk, capacity, participants, projector = request.GET.values()
#         # (pub_date__range=(start_date, end_date))
#         query = Auditorium.objects.filter(pk=pk, capacity__range=(participants, capacity), projector=projector).order_by('capacity')
#         if len(query) == 0:
#             return HttpResponse('Brak wolnych sal dla podanych kryteriów wyszukiwania')
#         else:
#             query = '<br>'.join(auditorium.name for auditorium in query)
#             search_parameters = '<br>'.join((pk, capacity, participants, projector))
#             return HttpResponse(f'{search_parameters}<br>{query}')