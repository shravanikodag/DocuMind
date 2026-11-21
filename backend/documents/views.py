from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services.RAG import ask_document

from .models import Document
from .serializers import DocumentSerializer

class DocumentUploadView(generics.ListCreateAPIView):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ask_question(request):

    document_id = request.data.get("document_id")
    question = request.data.get("question", "")

    if not isinstance(question, str) or not question.strip():
        return Response(
            {"error": "Please enter a question."},
            status=400
        )

    document = get_object_or_404(
        Document,
        id=document_id
    )

    try:
        result = ask_document(document, question.strip())
    except ValueError as error:
        return Response({"error": str(error)}, status=400)

    return Response(result)

