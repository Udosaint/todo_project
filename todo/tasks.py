from celery import shared_task

from django.core.mail import send_mail
from django.template.loader import render_to_string

from api.models import User
from todo.models import Todo



@shared_task(bind=True)
def test_func(self):
    send_mail("TESTING", 'TESTING MY MAIL', "noreply@tbnotes.com", ['udosaintdanielokoye@gmail.com'])
    return "Done"


@shared_task(bind=True)
def send_mail_pending_todo(self):
    #this function sends email to users showing them there pending/uncompleted todo task
    users = User.objects.all().exclude(username='admin') 
    for user in users:
        
        username = user.username
        todo = user.todo_set.all().filter(status=0)
        todo_count = user.todo_set.all().filter(status=0).count()
        html = render_to_string('todo/emails/uncomplete_todo.html',{
        'username':username,
        'todo_count':todo_count,
        'todo':todo
        })
        send_mail(
            'Uncompleted Task',
            f'Hi, {user.username}, you have {todo_count} uncompleted Todo',
            'noreply@tbnotes.com',
            [user.email],
            html_message=html
            )

    return "Done"