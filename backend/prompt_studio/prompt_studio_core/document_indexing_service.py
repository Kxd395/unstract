from typing import Optional

from django.conf import settings
from utils.cache_service import CacheService


class DocumentIndexingService:
    CACHE_PREFIX = "document_indexing:"

    @classmethod
    def set_document_indexing(cls, doc_id_key: str) -> None:
        CacheService.set_key(
            cls._cache_key(doc_id_key), "started", expire=settings.INDEXING_FLAG_TTL
        )

    @classmethod
    def is_document_indexing(cls, doc_id_key: str) -> bool:
        return CacheService.get_key(cls._cache_key(doc_id_key)) == b"started"

    @classmethod
    def mark_document_indexed(cls, doc_id_key: str, doc_id: str) -> None:
        CacheService.set_key(
            cls._cache_key(doc_id_key), doc_id, expire=settings.INDEXING_FLAG_TTL
        )

    @classmethod
    def get_indexed_document_id(cls, doc_id_key: str) -> Optional[str]:
        result = CacheService.get_key(cls._cache_key(doc_id_key))
        if result and result != b"started":
            return result.decode()  # Assuming doc_id is stored as a string
        return None

    @classmethod
    def remove_document_indexing(cls, doc_id_key: str) -> None:
        CacheService.delete_a_key(cls._cache_key(doc_id_key))

    @classmethod
    def _cache_key(cls, doc_id_key: str) -> str:
        return f"{cls.CACHE_PREFIX}{doc_id_key}"