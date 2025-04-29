import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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
        except Exception as exc:
            logger.error(f"Error creating transaction: {exc}", exc_info=True)
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
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
