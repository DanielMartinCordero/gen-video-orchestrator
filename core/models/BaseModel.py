from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, bridge):
        self.bridge = bridge  # Constructor

    @abstractmethod
    def generate_content(self, topic, workflow_data):
        """Mandatory method that each model has to implement"""
        pass