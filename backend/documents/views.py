from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from .models import Document
from .serializers import DocumentSerializer

class DocumentUploadView(generics.ListCreateAPIView):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
