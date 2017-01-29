from rest_framework.renderers import TemplateHTMLRenderer


class ListResultedTemplateHTMLRenderer(TemplateHTMLRenderer):

    def render(self, data, *args, **kwargs):
        if isinstance(data, list):
            data = {"results": data}

        return super().render(data, *args, **kwargs)