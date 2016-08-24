from django import forms
from .models import Blog, Product
from .signals import blog_audit

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

    def clean(self):
        cleaned_data = super(BlogForm, self).clean()
        if self.has_changed():
            blog_audit.send(sender=self.__class__)
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
