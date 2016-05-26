from django import forms
from .models import Blog

USER_BLACKLIST = ["test", "test2"]

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'body', 'timestamp', 'owner']

    def clean_owner(self):
	owner = self.cleaned_data['owner']
	if owner.username in USER_BLACKLIST:
	    raise forms.ValidationError("owner is not valid.")
	return owner
