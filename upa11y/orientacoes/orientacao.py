from dataclasses import dataclass, field
from typing import Callable


@dataclass
class RefatoracaoA11y:
    titulo: str
    descricao: str = ""
    codigo_refatoracao: str = ""
    funcao_refatoracao: str = "refatorar"
    refatorar: Callable | None = None


@dataclass
class OrientacaoA11y:
    num_orientacao: str
    descricao: str
    teste: Callable
    codigo_teste: str = ""
    funcao_teste: str = "testar"
    refatoracoes: tuple[RefatoracaoA11y, ...] = ()

    def rodar(self, parser):
        return self.teste(parser)


@dataclass
class ConjuntoOrientacoes:
    titulo: str = "Nenhum conjunto carregado"
    orientacoes: tuple[OrientacaoA11y, ...] = field(default_factory=tuple)
    codigo_utils: str = ""

    def __len__(self):
        return len(self.orientacoes)
