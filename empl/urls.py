from django.urls import path


from . import views
from .views import ShowTickets, ShowMyAktivTickets, TicketDetailView, AktivTicketDetailView, ShowClosedTicketsEmpl, \
    ShowWaitAcceptTicketsEmpl, AddManual, ShowAllManuals

urlpatterns = [

    path('pageemp/', ShowTickets.as_view(), name='pageemp'),
    path('manuals/', ShowAllManuals.as_view(), name='manuals'),# URL для представления ShowTickets
    path('show_ticket/', ShowMyAktivTickets.as_view(), name='show_ticket'),
    path('closed_tickets_empl/', ShowClosedTicketsEmpl.as_view(), name='closed_tickets_empl'),
    path('wait_accept_empl/', ShowWaitAcceptTicketsEmpl.as_view(), name='wait_accept_empl'),
    path('add_manual/', AddManual.as_view(), name='add_manual'),
    path('post/<slug:post_slug>/', views.ShowManual.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ManualCategory.as_view(), name='category'),
    path('post/', ShowTickets.as_view(), name='post'),
    path('ticket_detail/<int:ticket_id>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('aktiv_ticket_details/<int:ticket_id>/', AktivTicketDetailView.as_view(), name='aktiv_ticket_details'),



]
