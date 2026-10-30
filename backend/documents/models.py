from django.db import models


# Create your models here
class Document(models.Model):
    STATUS_CHOICES = [
        ("uploaded","Uploaded"),
        ("processing","Processing"),
        ("completed","Completed"),
        ("failed","Failed"),
    ]
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="uploaded",)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document,on_delete=models.CASCADE,related_name="chunks",)
    content = models.TextField()
    chunk_index = models.PositiveIntegerField()
    page_number = models.PositiveIntegerField(null=True,blank=True)

    class Meta:
        ordering = ["chunk_index"]
        constraints = [
            models.UniqueConstraint(
                fields=["document","chunk_index"],
                name="unique_document_chunk_index",
            )
        ]
    def __str__(self):
        return f"{self.document.title}-Chunk{self.chunk_index}"
    