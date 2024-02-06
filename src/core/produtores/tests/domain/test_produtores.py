import pytest

from src.core.produtores.domain.produtores import Produtores

#Como não está sendo utilizada a biblioteca unittest que é nativa do python, caso você esteja utilizando o vscode, na paleta de comando vá em "Python: Configure Tests", selecione pytest e então o root. Os testes podem ser executados a partir da barra de navagação na lateral esquerda, em Testing

class TestProdutores():
    def test_registroIndividual_is_required(self):
        with pytest.raises(TypeError):
            Produtores()

    def test_registroIndividual_have_less_than_14_characters(self):
        with pytest.raises(ValueError, match="Registro individual deve ter no máximo 14 caractéres"):
            Produtores(registroIndividual="a" * 15, nomeProdutor="teste", status=1)

    def test_cannot_create_produtores_with_empty_registroIndividual(self):
        with pytest.raises(ValueError, match="Registro Individual não pode ser vazio"):
            Produtores(registroIndividual="", nomeProdutor="Teste da Silva", status=1)


#Segue-se um padrão de testes chamado Given-When-Then, que subdivide os testes em 3 etapas: Arrange (Preparação) -> Act (Ação) -> Assert (Afirmação)
class TestUpdateProdutores:
    def test_update_produtores_with_name(self):
        #Arrange
        produtor = Produtores(registroIndividual="123.456.789-10", nomeProdutor="Teste da Silva", status=1)

        #Act
        produtor.update_produtores(nomeProdutor="Fulano da Silva")

        #Assert
        assert produtor.nomeProdutor == "Fulano da Silva"

    def test_cannot_update_produtores_with_empty_registroIndividual(self):
        with pytest.raises(ValueError, match="Registro Individual não pode ser vazio"):
            Produtores(registroIndividual="", nomeProdutor="Teste da Silva", status=1)

class TestChangeStatus:
    def test_activate_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= False,
        )

        produtor.activate()

        assert produtor.status is True

    def test_deactivate_produtores(self):
        produtor = Produtores(
            nomeProdutor= "Teste da Silva",
            registroIndividual= "123.456.789-10",
            status= True,
        )

        produtor.deactivate()

        assert produtor.status is False