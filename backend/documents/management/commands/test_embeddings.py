
from django.core.management.base import BaseCommand

from documents.models import Document, DocumentChunk
from documents.services.embeddings import EmbeddingService


class Command(BaseCommand):

    help = "Test embedding generation for saved document chunks"

    def handle(self, *args, **options):

        document = Document.objects.first()

        if document is None:
            self.stdout.write("No uploaded document found.")
            return

        chunks = list(
            DocumentChunk.objects.filter(
                document=document
            ).order_by("chunk_index")
        )

        if not chunks:
            self.stdout.write("No chunks found.")
            return

        texts = [chunk.content for chunk in chunks]

        embedding_service = EmbeddingService()

        embeddings = embedding_service.generate_embeddings(texts)

        self.stdout.write(
            f"Total chunks: {len(chunks)}"
        )

        self.stdout.write(
            f"Embedding shape: {embeddings.shape}"
        )

        self.stdout.write(
            f"Vector dimensions: {embeddings.shape[1]}"
        )

        self.stdout.write(
            "Embedding generation successful!"
        )
