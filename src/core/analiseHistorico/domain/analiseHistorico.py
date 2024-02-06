from dataclasses import dataclass, field
from datetime import datetime

import uuid

@dataclass
class AnaliseHistorico:
    numeroCar: str
    nomePropriedade: str
    dateAnalise: datetime = field(default_factory=datetime.now)
    idAnaliseHistorico: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.numeroCar:
            raise ValueError("NumeroCar não pode ser vazio")
        
        
    def __str__(self):
        return f"{self.numeroCar} - {self.nomePropriedade} ({self.dateAnalise})"
    
    def __repr__(self):
        return f"<Produtores {self.nomePropriedade} ({self.idAnaliseHistorico})>"

    def __eq__(self, other):  # a == b -> a.__eq__(b)
        if not isinstance(other, AnaliseHistorico):
            return False

        return self.idAnaliseHistorico == other.idAnaliseHistorico
