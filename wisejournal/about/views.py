from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about_author.html'


class AboutSpecView(TemplateView):
    template_name = 'about/about_spec.html'
