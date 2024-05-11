from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from empl.forms import AddPostManual
from empl.models import Manuals, Category
from helpdesk.forms import AddPostForm
from helpdesk.models import Ticket
from users.models import User


# Create your views here.

def has_role3(user):
    if user.is_authenticated:
        return user.role_id == 3
    return False


class ShowAllManuals(LoginRequiredMixin, ListView):
    template_name = 'empl/manuals.html'
    context_object_name = 'posts'
    title_page = 'Руководства'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cat = self.request.GET.get('cat')

            if cat:
                queryset = Manuals.objects.filter(cat_id=cat)
            else:
                queryset = Manuals.objects.all()

            return queryset
        else:
            return Manuals.objects.none()

    # def get_queryset(self):
    #     return Manuals.objects.all()


class AddManual(LoginRequiredMixin, CreateView):
    form_class = AddPostManual
    template_name = 'empl/add_manual.html'
    title_page = 'Добавление статьи'
    success_url = reverse_lazy('manuals')

    # метод get_context_data для передачи дополнительных данных в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


class ShowManual(DetailView):
    template_name = 'empl/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Manuals.objects.all(), slug=self.kwargs[self.slug_url_kwarg])


class ManualCategory(LoginRequiredMixin, ListView):
    template_name = 'empl/manual.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Manuals.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


class ShowMyAktivTickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'empl/show_ticket.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='В процессе', empl=self.request.user)

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
            ticket.status = 'Ожидает подтверждения'
            ticket.save()
            return redirect('show_ticket')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


class ShowTickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'empl/pageemp.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='активная')

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
            ticket.status = 'В процессе'
            ticket.save()
            return redirect('show_ticket')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


class ShowWaitAcceptTicketsEmpl(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'empl/wait_accept_empl.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='Ожидает подтверждения', empl=self.request.user)

            sort = self.request.GET.get('sort')

            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе</h1>")
        return super().dispatch(request, *args, **kwargs)


class ShowClosedTicketsEmpl(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'empl/closed_tickets_empl.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(status='Выполнена', empl=self.request.user)
            sort = self.request.GET.get('sort')
            if sort == 'earliest':
                queryset = queryset.order_by('opened_date')
            elif sort == 'latest':
                queryset = queryset.order_by('-opened_date')

            return queryset
        else:
            return Ticket.objects.none()


class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'empl/ticket_detail.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        if 'ticket_id' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.empl = request.user
            ticket.status = 'В процессе'
            ticket.save()
            return redirect('show_ticket')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


class AktivTicketDetailView(LoginRequiredMixin, View):
    template_name = 'empl/aktiv_ticket_details.html'

    def get(self, request, ticket_id, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        if 'ticket_id' in request.POST:
            ticket_id = request.POST.get('ticket_id')
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.empl = request.user
            ticket.status = 'активная'
            ticket.save()
            return redirect('show_ticket')
        else:
            return render(request, 'error.html', {'message': 'Invalid request'})

    def dispatch(self, request, *args, **kwargs):
        if not has_role3(request.user):
            return HttpResponse("<h1>Отказано в доступе </h1>")  # Возврат пользователю сообщения об отказе в доступе
        return super().dispatch(request, *args, **kwargs)


