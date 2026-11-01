
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "uploaded_at",
            "status",
        ]
        read_only_fields = ["id", "uploaded_at", "status"]

    def validate_file(self, value):
        # Maximum file size: 10 MB
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size cannot exceed 10 MB."
            )

        # Validate file extension
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are allowed."
            )

        # Validate PDF file signature
        header = value.read(5)
        value.seek(0)

        if header != b"%PDF-":
            raise serializers.ValidationError(
                "Invalid PDF file."
            )

        return value
