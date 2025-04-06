from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model

from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    
    if date:
        order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: str = None) -> list[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return list(queryset) 