from dataclasses import dataclass

@dataclass
class OrientacaoA11y:
    num_orientacao: str
    descricao: str
    tags_alvo: list
    teste: object
    refatoracao: object = None