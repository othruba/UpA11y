from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from upa11y.orientacoes.orientacao import ConjuntoOrientacoes, OrientacaoA11y, RefatoracaoA11y

FORMATO_ORIENTACOES = "upa11y.orientacoes.codigo"
VERSAO_FORMATO = 2


@dataclass
class AmbienteExecucao:
    origem: str
    codigo_utils: str = ""
    globais: dict[str, Any] = field(init=False)

    def __post_init__(self) -> None:
        self.globais = {"__name__": "__upa11y_utils__"}
        if self.codigo_utils.strip():
            exec(compile(self.codigo_utils, f"{self.origem}:utils", "exec"), self.globais)

    def executar(self, codigo: str, nome: str) -> dict[str, Any]:
        namespace = dict(self.globais)
        exec(compile(codigo, nome, "exec"), namespace)
        return namespace

    @classmethod
    def com_globais(cls, origem: str, globais: dict) -> AmbienteExecucao:
        ambiente = cls.__new__(cls)
        ambiente.origem = origem
        ambiente.codigo_utils = ""
        ambiente.globais = globais
        return ambiente


@dataclass(frozen=True)
class SerializadorOrientacoes:
    formato: str = FORMATO_ORIENTACOES
    versao: int = VERSAO_FORMATO

    def importar(self, caminho: str | Path) -> ConjuntoOrientacoes:
        arquivo = Path(caminho)
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
        return self.de_dict(dados, arquivo)

    def exportar(self, conjunto: ConjuntoOrientacoes, caminho: str | Path) -> Path:
        arquivo = Path(caminho)
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(
            json.dumps(self.para_dict(conjunto), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return arquivo

    def de_dict(self, dados: dict, origem: Path | str = "<json>") -> ConjuntoOrientacoes:
        origem = str(origem)
        utils = dados.get("utils", "")
        ambiente = AmbienteExecucao(origem=origem, codigo_utils=utils)
        orientacoes = [
            self._criar_orientacao(item, ambiente)
            for item in dados.get("orientacoes", [])
        ]

        return ConjuntoOrientacoes(
            titulo=dados.get("titulo", "Conjunto sem título"),
            codigo_utils=utils,
            orientacoes=tuple(orientacoes),
        )

    def para_dict(self, conjunto: ConjuntoOrientacoes) -> dict:
        return {
            "formato": self.formato,
            "versao": self.versao,
            "titulo": conjunto.titulo,
            "utils": conjunto.codigo_utils,
            "orientacoes": [self._orientacao_para_dict(orientacao) for orientacao in conjunto.orientacoes],
        }

    def _criar_orientacao(self, dados: dict, ambiente: AmbienteExecucao) -> OrientacaoA11y:
        codigo = dados.get("codigo", "")
        funcao = dados.get("funcao", "testar")
        namespace = ambiente.executar(codigo, f"{ambiente.origem}:{dados.get('num_orientacao', 'teste')}")
        refatoracoes = [
            self._criar_refatoracao(item, ambiente)
            for item in dados.get("refatoracoes", [])
        ]

        return OrientacaoA11y(
            num_orientacao=dados.get("num_orientacao", ""),
            descricao=dados.get("descricao", ""),
            teste=namespace[funcao],
            codigo_teste=codigo,
            funcao_teste=funcao,
            refatoracoes=tuple(refatoracoes),
        )

    def _orientacao_para_dict(self, orientacao: OrientacaoA11y) -> dict:
        return {
            "num_orientacao": orientacao.num_orientacao,
            "descricao": orientacao.descricao,
            "funcao": orientacao.funcao_teste,
            "codigo": orientacao.codigo_teste,
            "refatoracoes": [self._refatoracao_para_dict(refatoracao) for refatoracao in orientacao.refatoracoes],
        }

    def _criar_refatoracao(self, dados: dict, ambiente: AmbienteExecucao) -> RefatoracaoA11y:
        codigo = dados.get("codigo", "")
        funcao = dados.get("funcao", "refatorar")
        refatorar = None
        if codigo.strip():
            namespace = ambiente.executar(codigo, f"{ambiente.origem}:{dados.get('titulo', 'refatoracao')}")
            refatorar = namespace.get(funcao)

        return RefatoracaoA11y(
            titulo=dados.get("titulo", ""),
            descricao=dados.get("descricao", ""),
            codigo_refatoracao=codigo,
            funcao_refatoracao=funcao,
            refatorar=refatorar,
        )

    @staticmethod
    def _refatoracao_para_dict(refatoracao: RefatoracaoA11y) -> dict:
        return {
            "titulo": refatoracao.titulo,
            "descricao": refatoracao.descricao,
            "funcao": refatoracao.funcao_refatoracao,
            "codigo": refatoracao.codigo_refatoracao,
        }


def importar_conjunto(caminho: str | Path) -> ConjuntoOrientacoes:
    return SerializadorOrientacoes().importar(caminho)


def exportar_conjunto(conjunto: ConjuntoOrientacoes, caminho: str | Path) -> Path:
    return SerializadorOrientacoes().exportar(conjunto, caminho)


def conjunto_de_dict(dados: dict, origem: Path | str = "<json>") -> ConjuntoOrientacoes:
    return SerializadorOrientacoes().de_dict(dados, origem)


def conjunto_para_dict(conjunto: ConjuntoOrientacoes) -> dict:
    return SerializadorOrientacoes().para_dict(conjunto)


def criar_orientacao(dados: dict, globais: dict, origem: str) -> OrientacaoA11y:
    ambiente = AmbienteExecucao.com_globais(origem, globais)
    return SerializadorOrientacoes()._criar_orientacao(dados, ambiente)


def orientacao_para_dict(orientacao: OrientacaoA11y) -> dict:
    return SerializadorOrientacoes()._orientacao_para_dict(orientacao)


def criar_refatoracao(dados: dict, globais: dict, origem: str) -> RefatoracaoA11y:
    ambiente = AmbienteExecucao.com_globais(origem, globais)
    return SerializadorOrientacoes()._criar_refatoracao(dados, ambiente)


def refatoracao_para_dict(refatoracao: RefatoracaoA11y) -> dict:
    return SerializadorOrientacoes()._refatoracao_para_dict(refatoracao)


def compilar_utils(codigo: str, origem: str) -> dict:
    return AmbienteExecucao(origem=origem, codigo_utils=codigo).globais


def executar_codigo(codigo: str, globais: dict, nome: str) -> dict:
    namespace = dict(globais)
    exec(compile(codigo, nome, "exec"), namespace)
    return namespace
