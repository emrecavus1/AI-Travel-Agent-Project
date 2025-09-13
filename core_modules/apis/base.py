from abc import ABC, abstractmethod

class APIBase(ABC):
    """Abstract base class for all API connectors."""

    @abstractmethod
    def supports(self, category: str) -> bool:
        """Check if this API supports a category."""
        pass

    @abstractmethod
    def search(self, location: str, category: str, budget: float):
        """Search for items given a location, category, and budget."""
        pass
