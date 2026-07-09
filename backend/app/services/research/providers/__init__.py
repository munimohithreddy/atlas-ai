from app.services.research.providers.base import (
    EvidenceSignal,
    ResearchProvider,
    ResearchProviderResult,
)
from app.services.research.providers.affiliate import AffiliateProgramResearchProvider
from app.services.research.providers.manual import ManualEvidenceProvider
from app.services.research.providers.mock import MockResearchProvider

__all__ = [
    "AffiliateProgramResearchProvider",
    "EvidenceSignal",
    "ManualEvidenceProvider",
    "MockResearchProvider",
    "ResearchProvider",
    "ResearchProviderResult",
]
