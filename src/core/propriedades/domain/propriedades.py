from dataclasses import dataclass, field
import uuid

@dataclass
class Propriedades:
    class StatusLiberado:
        BLOQUEADO = 0
        LIBERADO = 1
        ALERTA = 2

    nomePropriedade: str
    numeroCar: str
    uf: str
    municipio: str
    pais: str
    liberado: int = StatusLiberado.BLOQUEADO
    status: bool = True
    idPropriedade: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.nomePropriedade) > 255:
            raise ValueError("Nome da propriedade deve ter no máximo 255 caractéres")
        
        if not self.nomePropriedade:
            raise ValueError("Nome da propriedade não pode ser vazio")
        
    def __str__(self):
        return f"{self.nomePropriedade} - {self.uf} ({self.status})"
    
    def __repr__(self):
        return f"<Propriedades {self.nomePropriedade} ({self.idPropriedade})>"

    def __eq__(self, other):
        if not isinstance(other, Propriedades):
            return False
        return self.idPropriedade == other.idPropriedade
    
    def update_propriedades(self, liberado):
        self.liberado = liberado

        self.validate()
    
    def activate(self):
        self.status = True

        self.validate()

    def deactivate(self):
        self.status = False

        self.validate()