from collections.abc import Sequence
from dataclasses import dataclass

from upa11y.orientacoes.orientacao import OrientacaoA11y


@dataclass
class Refatorador:
    orientacoes: Sequence[OrientacaoA11y]

    def rodar(self, parser):
        problemas = []
        for orientacao in self.orientacoes:
            problemas.extend(orientacao.rodar(parser))

        return problemas
