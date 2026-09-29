from upa11y.orientacoes.orientacao import ConjuntoOrientacoes, OrientacaoA11y, RefatoracaoA11y
from upa11y.orientacoes.serializacao import (
    AmbienteExecucao,
    SerializadorOrientacoes,
    exportar_conjunto,
    importar_conjunto,
)

CONJUNTO_VAZIO = ConjuntoOrientacoes(
    titulo="Nenhum conjunto carregado",
    orientacoes=(),
)

__all__ = [
    "CONJUNTO_VAZIO",
    "ConjuntoOrientacoes",
    "OrientacaoA11y",
    "RefatoracaoA11y",
    "AmbienteExecucao",
    "SerializadorOrientacoes",
    "exportar_conjunto",
    "importar_conjunto",
]
