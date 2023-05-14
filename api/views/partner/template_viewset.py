from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class TemplateViewSet(GenericViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'])
    def about(self, request):
        return Response(template_name='pw_partner_about.html')

    @action(detail=False, methods=['GET'], url_path='terms-and-conditions')
    def termsAndConditions(self, request):
        return Response(template_name='pw_partner_terms.html')
