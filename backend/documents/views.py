from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services.RAG import ask_document
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.exceptions import ValidationError
from documents.models import DocumentChunk
from documents.services.pdf_processor import PDFProcessor
from documents.services.chunking import TextChunker

class DocumentUploadView(generics.ListCreateAPIView):

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        document = serializer.save(status="processing")

        try:
            pages = PDFProcessor.extract_text(document.file.path)
            chunks = TextChunker.chunk_pages(pages)
            if not chunks:
                raise ValueError("No text found in PDF.")
            DocumentChunk.objects.bulk_create([
                DocumentChunk(
                    document=document,
                    content=chunk["content"],
                    chunk_index=chunk["chunk_index"],
                    page_number=chunk["page_number"]
                )
                for chunk in chunks
            ])

        except ValueError as error:
            document.status = "faild"
            document.save(update_fields=["status"])
            raise ValidationError({"file":str(error)})
        document.status = "completed"
        document.save(update_fields=["status"])
            

        





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

