from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rezerwacje.models import Auditorium, Reservation
from django.utils.timezone import datetime

def room(request, id_):
    the_room = Auditorium.objects.get(pk=id_)
    result = f"""
    <html><body>
    <h1>{the_room.name}</h1><hr>
    <h3>This room can fit up to {the_room.capacity} people.</h3>"""
    if the_room.projector:
        result += '<h3>Our auditorium is equipped with a projector.</h3>'
    result += '<h3>Occupied:</h3><ul><h4>'
    for reservation in Reservation.objects.filter(auditorium_id=id_):
        result += f'<li>{reservation.date}.<br>'
        if reservation.comment:
            result += f'Comment: {reservation.comment}.</li>'
    result += '</h4></ul>' \
              f'<a href="http://127.0.0.1:8000/reserve/{the_room.id}">' \
              '<input type="submit" value="Reserve"</a>' \
              f'<a href="http://127.0.0.1:8000/edit/{the_room.id}">' \
              '<input type="submit" value="Edit"</a>' \
              f'<a href="http://127.0.0.1:8000/delete/{the_room.id}">' \
              '<input type="submit" value="Delete"</a></body></html>'
    return HttpResponse(result)


def reserve(request, id_):
    the_room = Auditorium.objects.get(pk=id_)
    if request.method == 'GET':
        response = f"""
                    <html> <body>
                        <form action="#" method="POST">
                        <h2>Reserve {the_room.name}</h2>
                        <h3><label>
                            When: <input type="date" name="date"/>
                            Leave a comment: <input type="text" name="comment"/>
                            <input type="submit" value="Reserve"/>
                        </label></h3>
                        <h3> Please keep in mind, that this room is already occupied:</h3><h4>"""
        for reservation in Reservation.objects.filter(auditorium_id=id_):
            response += f'<li>{reservation.date}.<br>'
        response += "</h4></body></html>"
        return HttpResponse(response)
    if request.method == 'POST':
        date = request.POST['date']
        try:
            new_reservation = Reservation.objects.create(date=date, auditorium_id=the_room.id)
        except IntegrityError:
            return HttpResponse('This room is unavailable at this time.')
        the_date = datetime.strptime(new_reservation.date, '%Y-%m-%d').date()
        if the_date < datetime.today().date():
            return HttpResponse("Don't fuck with me, mate.")
        if 'comment' in request.POST:
            new_reservation.comment = request.POST['comment']
            new_reservation.save()
        return redirect('/')


def room_list(request):
    today = datetime.today()
    table = ""
    for room in Auditorium.objects.order_by('id'):
        table += '<tr>'
        table += '<td> {} </td><td><a href="/room/{}"> {} </a></td>'\
            .format(room.pk, room.pk, room.name)
        if Reservation.objects.filter(auditorium_id=room.pk, date=today).exists():
            table += '<td> Dziś zarezerwowana </td>'
        else:
            table += '<td> Dziś wolna </td>'
        table += '<td><a href="/reserve/{}"> Zarezerwuj salę </a></td>' \
                 '<td><a href="/edit/{}"> Wyedytuj salę </a></td>' \
                 '<td><a href="/delete/{}"> Usuń salę </a></td></tr>'\
            .format(room.pk, room.pk, room.pk)

    response = """
    <html><body>
    <br>
    <a href="/search/make-search"><input type="button" value="Przejdź do wyszukiwarki"/></a><br>
    <br>
    <table border = 1px>
    {}
    </table>
    <br>
    <a href="/add_room"><input type="button" value="Dodaj salę"/></a>
    </body></html>
    """.format(table)
    return HttpResponse(response)


def add_room(request):
    if request.method == "GET":
        response = """
            <html>
            <body>
            <form action="" method="POST">
                <label>
                Nazwa sali <input type="text" name="name"/>
                </label>
                <label>
                Max pojemność <input type="number" name="capacity"/>
                </label>
                <select name='projector'>
                <option value> -- select an option -- </option>
                <option value='True'> Jest projektor </option>
                <option value='False'> Nie ma projektora </option>
                </select>
                <input type="submit" value="Dodaj"/>
            </form>
            </body>
            </html>
            """
        return HttpResponse(response)
    else:
        name = request.POST["name"]
        capacity = int(request.POST["capacity"])
        projector = request.POST["projector"]
        new_room = Auditorium.objects.create(name=name, capacity=capacity, projector=projector)
        return HttpResponse("Sukces! Dodano salę {} mięszczącą {} osób, rzutnik: {}"
                            "<br><a href='/'>[Wróć do listy]</a>"
                            .format(new_room.name, new_room.capacity, new_room.projector))


def edit_room(request, id):
    room = Auditorium.objects.get(pk=id)
    if request.method == "GET":
        response = """
            <html>
            <body>
            <p>Możesz zmienić dane dla {}.</p><br>
            <form action="" method="POST">
                <label>
                Nazwa sali <input type="text" name="name" value="{}"/>
                </label>
                <label>
                Max pojemność <input type="number" name="capacity" value="{}"/>
                </label>
                <select name='projector' value="{}">
                <option value> -- select an option -- </option>
                <option value='True'> Jest projektor </option>
                <option value='False'> Nie ma projektora </option>
                </select>
                <input type="submit" value="Dodaj"/>
            </form>
            </body>
            </html>
            """.format(room.name, room.name, room.capacity, room.projector)
        return HttpResponse(response)
    else:
        new_name = request.POST["name"]
        new_capacity = int(request.POST["capacity"])
        new_projector = request.POST["projector"]
        room.name = new_name
        room.capacity = new_capacity
        room.projector = new_projector
        room.save()
        return HttpResponse("Sukces! Zapisano salę {} mięszczącą {} osób, rzutnik: {}"
                            "<br><a href='/'>[Wróć do listy]</a>"
                            .format(room.name, room.capacity, room.projector))


def del_room(request, id):
    temp = Auditorium.objects.get(pk=id)
    response = "Sukces! Salę {} usunięto z bazy." \
               "<br><a href='/'>[Wróć do listy]</a>".format(temp.name)
    temp.delete()
    return HttpResponse(response)