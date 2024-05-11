from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from .views import ShowTickets

urlpatterns = [

    path('mainpageusers/', views.AddPage.as_view(), name='mainpageusers'),
    path('mytickets/', views.ShowMyAktivTicketsUser.as_view(), name='mytickets'),
    path('wait_accept/', views.ShowWaitAcceptTickets.as_view(), name='wait_accept'),
    path('closed_tickets_user/', views.ShowClosedTickets.as_view(), name='closed_tickets_user'),
    path('contakts/', views.ShowContacts.as_view(), name='contakts'),
    path('ticket/<int:ticket_id>/report/', views.AddReport.as_view(), name='add_report'),
    path('helpdesk/ticket/<int:pk>/edit/', views.UpdatePage.as_view(), name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('my_ticket_detail/<int:ticket_id>/', views.MyTicketDetailView.as_view(), name='my_ticket_detail'),
    path('show_technik/<int:ticket_id>/', views.ShowTechnik.as_view(), name='show_technik'),
    path('wait_accept_detail/<int:ticket_id>/', views.MyTicketWaitAcceptDetail.as_view(), name='wait_accept_detail'),
    path('report_detail/<int:report_id>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('notexit/', views.AddPage.as_view(), name='notexit'),
    path('notexit/', views.ShowTickets.as_view(), name='notexit'),


]


