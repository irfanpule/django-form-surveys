from django.views.generic.base import ContextMixin


class ContextTitleMixin(ContextMixin):
    title_page = ''

    def get_title_page(self):
        return self.title_page

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form' not in kwargs:
            kwargs['title'] = self.get_title_page()
            kwargs['title_page'] = self.get_title_page()
        return super().get_context_data(**kwargs)
