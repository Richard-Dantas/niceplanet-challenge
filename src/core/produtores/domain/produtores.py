from dataclasses import dataclass, field
import uuid

@dataclass
class Produtores:
    registroIndividual: str
    nomeProdutor: str
    status: bool = True
    #Basicamente aqui diz que em idProdutor, caso o valor não seja passado na construção do objeto, será gerado um identificador único universal, que possui algumas vantagens até mesmo em questão de segurança em relação à IDs incrementais como 1, 2, 3...
    idProdutor: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.registroIndividual) > 14:
            raise ValueError("Registro individual deve ter no máximo 14 caractéres")
        
        if not self.registroIndividual:
            raise ValueError("Registro Individual não pode ser vazio")
        
        
    def __str__(self):
        return f"{self.nomeProdutor} - {self.registroIndividual} ({self.status})"
    
    def __repr__(self):
        return f"<Produtores {self.nomeProdutor} ({self.idProdutor})>"

    def __eq__(self, other):  # a == b -> a.__eq__(b)
        if not isinstance(other, Produtores):
            return False

        return self.idProdutor == other.idProdutor
    
    def update_produtores(self, nomeProdutor):
        self.nomeProdutor = nomeProdutor

        self.validate()
    
    def activate(self):
        self.status = True

        self.validate()

    def deactivate(self):
        self.status = False

        self.validate()