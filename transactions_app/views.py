import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from .models import Transaction
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)


class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except ValidationError as exc:
            # exc.detail is a dict of field errors
            logger.error(f"Validation failed: {exc.detail}", exc_info=True)
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}", exc_info=True)
            return Response(
                {"detail": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise NotFound(
                detail=f"Transaction with id={pk} not found",
                code=status.HTTP_404_NOT_FOUND
            )
