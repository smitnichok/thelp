from datetime import datetime

from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views import View

from empl.models import Manuals
from helpdesk.forms import AddPostForm, TicketForm, ReportForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import redirect, get_object_or_404, render

from users.models import User
from .models import Ticket, Report


def has_role2(user):
    if user.is_authenticated:
        return user.role_id == 2
    return False


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'helpdesk/mainpageusers.html'
    login_url = '/login/'

    def form_valid(self, form):
        t = form.save(commit=False)
        t.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not has_role2(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


class ShowTickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'helpdesk/mytickets.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = Ticket.objects.filter(user=user, status='активная')
            sort = self.request.GET.get('sort')

            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()

    # def post(self, request, *args, **kwargs):
    #     if 'ticket_id' in request.POST:
    #         ticket_id = request.POST.get('ticket_id')
    #         ticket = Ticket.objects.get(id=ticket_id)
    #         ticket.empl = request.user
    #         ticket.status = 'Выполнена'
    #         ticket.save()
    #         return redirect('mytickets')
    #     else:
    #         return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role2(request.user):
            return HttpResponse("<h1>Отказано в доступе</h1>")
        return super().dispatch(request, *args, **kwargs)


class ShowWaitAcceptTickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'helpdesk/wait_accept.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = Ticket.objects.filter(user=user, status='Ожидает подтверждения')

            sort = self.request.GET.get('sort')

            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()

    def post(self, request, *args, **kwargs):
        if 'ticket_id' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.closed_date = datetime.now().date()
            ticket.status = 'Выполнена'
            ticket.save()
            return redirect('mytickets')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role2(request.user):
            return HttpResponse("<h1>Отказано в доступе</h1>")
        return super().dispatch(request, *args, **kwargs)


class MyTicketDetailView(LoginRequiredMixin, View):
    template_name = 'helpdesk/my_ticket_detail.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {'ticket': ticket})


class MyTicketWaitAcceptDetail(LoginRequiredMixin, View):
    template_name = 'helpdesk/wait_accept_detail.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {'ticket': ticket})


def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.status == 'активная' or ticket.status == 'В процессе':
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect('mytickets')  # Перенаправление на страницу просмотра заявки
        else:
            form = TicketForm(instance=ticket)

        return render(request, 'helpdesk/edit_ticket.html', {'form': form})
    else:
        return HttpResponse("<h1>Отказано в доступе</h1>")


class ShowClosedTickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'helpdesk/closed_tickets_user.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='Выполнена', user=self.request.user)
            sort = self.request.GET.get('sort')
            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()


class ShowMyAktivTicketsUser(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'helpdesk/mytickets.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='активная', user=self.request.user)
            sort = self.request.GET.get('sort')
            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()

    def post(self, request, *args, **kwargs):
        if 'ticket_id' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.empl = request.user
            ticket.status = 'Выполнена'
            ticket.save()
            return redirect('closed_tickets_user')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role2(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.delete()
    return redirect('mytickets')


class AddReport(LoginRequiredMixin, CreateView):
    form_class = ReportForm
    template_name = 'helpdesk/add_report.html'

    def form_valid(self, form):
        report = form.save(commit=False)
        report.user = self.request.user
        report.save()

        ticket_id = self.request.POST.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=int(ticket_id))
            ticket.empl = self.request.user
            ticket.status = 'Выполнена'
            ticket.save()
            return redirect('mytickets')
        except (ValueError, Ticket.DoesNotExist):
            return HttpResponseBadRequest("Invalid ticket ID")


class ReportDetailView(LoginRequiredMixin, View):
    template_name = 'helpdesk/report_detail.html'

    def get(self, request, report_id, *args, **kwargs):
        report = get_object_or_404(Report, id=report_id)
        return render(request, self.template_name, {'report': report})


class ShowContacts(LoginRequiredMixin, ListView):
    model = User
    template_name = 'helpdesk/contakts.html'

    def get_queryset(self):
        queryset = User.objects.filter(role_id=3)
        return queryset


class ShowTechnik(LoginRequiredMixin, ListView):
    template_name = 'helpdesk/show_technik.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {'ticket': ticket})
def get_queryset(self):
    queryset = User.objects.filter(role_id=3)
    return queryset


class UpdatePage(UpdateView):
    model = Ticket
    fields = ['title', 'equipment', 'description', 'type', 'priority']
    template_name = 'helpdesk/mainpageusers.html'
    success_url = reverse_lazy('mytickets')
    title_page = 'Редактирование статьи'

# def show_contacts(request):
#     return render(request, 'helpdesk/contakts.html')
 