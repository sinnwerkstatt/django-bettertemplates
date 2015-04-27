from django.views.generic.base import TemplateView

class ExampleListView(TemplateView):
    template_name = 'example/example.html'
    
example_view = ExampleListView.as_view()


