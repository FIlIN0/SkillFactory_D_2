from django.template.loader import render_to_string

from django.core.mail.message import EmailMultiAlternatives


def get_subscriber(category):
    user_email = []
    for user in category.subscribers.all():
        user_email.append(user.email)
    return user_email


def new_post_subscription(instance):
    template = 'flatpages/mail/new_post.html'

    for category in instance.categories.all():
        email_subject = f'New post in category: "{category}"'
        user_emails = get_subscriber(category)

        html = render_to_string(
            template_name=template,
            context={
                'category': category,
                'post': instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email='tani4400@yandex.ru',
            to=user_emails
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


