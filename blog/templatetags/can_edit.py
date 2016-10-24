from django import template
register = template.Library()

@register.filter
def can_edit(user, blog):
    user_can_edit = False

    if user.is_authenticated:
        if user.is_superuser:
            user_can_edit = True
        else:
            if blog and blog.owner and blog.owner == user:
                user_can_edit = True
    return user_can_edit
