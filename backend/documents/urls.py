from django.urls import path
from .views import DocumentUploadView, ask_question

urlpatterns = [
    path(
        "documents/",
        DocumentUploadView.as_view(),
        name="document-upload",
    ),
    path(
        "ask/",
        ask_question,
        name="ask-question"
    ),
]