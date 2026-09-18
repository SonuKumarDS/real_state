from abc import ABC, abstractmethod

class LeadConnector(ABC):
    name = "base"

    @abstractmethod
    def discover(self, **filters):
        """Return only data the connector is authorized to access."""
        raise NotImplementedError

class CSVConnector(LeadConnector):
    name = "csv"
    def discover(self, rows=None, **filters):
        return rows or []

class AuthorizedAPIConnector(LeadConnector):
    """Template for an official/licensed API integration."""
    name = "authorized_api"
    def __init__(self, client):
        self.client = client
    def discover(self, **filters):
        return self.client.search(**filters)
