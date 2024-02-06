from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Vinculos:
    idPropriedade: UUID
    idProdutor: UUID
    idVinculo: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):  
        if not self.idPropriedade:
            raise ValueError("ID da propriedade não pode ser vazio")

    def __str__(self):
        return f"{self.idVinculo} - {self.idPropriedade} ({self.idProdutor})"
    
    def __repr__(self):
        return f"<Vinculos {self.idPropriedade} ({self.idProdutor})>"

    def __eq__(self, other):
        if not isinstance(other, Vinculos):
            return False
        return self.idVinculo == other.idVinculo