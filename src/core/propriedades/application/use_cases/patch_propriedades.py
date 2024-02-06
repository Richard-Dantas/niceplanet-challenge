from dataclasses import dataclass
from uuid import UUID
from core.propriedades.application.exceptions import PropriedadesNotFound

from core.propriedades.domain.IRepository.propriedades_repository import PropriedadesRepository


@dataclass
class PatchPropriedadesRequest:
    idPropriedade: UUID
    liberado: int

class PatchPropriedades:
    def __init__(self, repository: PropriedadesRepository):
        self.repository = repository

    def execute(self, request: PatchPropriedadesRequest) -> None:
        propriedade = self.repository.get_by_id(request.idPropriedade)

        propriedade.liberado = request.liberado

        propriedade.update_propriedades(liberado= propriedade.liberado)
        self.repository.update(propriedade)