from parser.parser import Parser
from orientacoes.lista_orientacoes import ORIENTACOES
from refatoracao.refatorador import Refatorador

html = open("sample/index.html", "r").read()

parser = Parser(html)
parser.criar_ids()

refatorador = Refatorador(ORIENTACOES)
problemas = refatorador.rodar(parser.obter_elementos())

print("Problemas encontrados:")
for problema in problemas:
    print(problema)