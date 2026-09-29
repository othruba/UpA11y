from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from upa11y.orientacoes.orientacao import OrientacaoA11y
from upa11y.parser.parser import Parser

EXTENSOES_HTML = {".html", ".htm"}


@dataclass
class AchadoA11y:
    recomendacao: str
    severidade: str
    elemento: str
    problema: str
    sugestao: str


@dataclass
class ResultadoArquivo:
    caminho: Path
    achados: list[AchadoA11y] = field(default_factory=list)
    erro: str = ""

    @property
    def total_achados(self) -> int:
        return len(self.achados)

    @property
    def contagem_severidade(self) -> Counter:
        return Counter(achado.severidade for achado in self.achados)

    def caminho_relativo(self, origem: Path) -> str:
        base = origem if origem.is_dir() else origem.parent
        return str(self.caminho.relative_to(base))


@dataclass
class ResultadoAnalise:
    origem: Path
    arquivos: list[ResultadoArquivo] = field(default_factory=list)
    erros: list[str] = field(default_factory=list)

    @property
    def arquivos_processados(self) -> int:
        return len([arquivo for arquivo in self.arquivos if not arquivo.erro])

    @property
    def total_achados(self) -> int:
        return sum(arquivo.total_achados for arquivo in self.arquivos)

    @property
    def contagem_severidade(self) -> Counter:
        contagem = Counter()
        for arquivo in self.arquivos:
            contagem.update(arquivo.contagem_severidade)
        return contagem


@dataclass(frozen=True)
class LocalizadorHtml:
    extensoes: frozenset[str] = field(default_factory=lambda: frozenset(EXTENSOES_HTML))

    def encontrar(self, caminho: str | Path) -> list[Path]:
        caminho = Path(caminho)
        if caminho.is_file() and caminho.suffix.lower() in self.extensoes:
            return [caminho]
        if caminho.is_dir():
            return sorted(
                arquivo
                for arquivo in caminho.rglob("*")
                if arquivo.suffix.lower() in self.extensoes
            )
        return []


@dataclass(frozen=True)
class FabricaAchado:
    def criar(self, dados, orientacao: OrientacaoA11y) -> AchadoA11y:
        if not isinstance(dados, dict):
            dados = {"problem": str(dados)}

        return AchadoA11y(
            recomendacao=dados.get("rec", orientacao.num_orientacao),
            severidade=dados.get("severity", "warning"),
            elemento=dados.get("element", "document"),
            problema=dados.get("problem", ""),
            sugestao=dados.get("suggestion", ""),
        )


@dataclass
class AnalisadorA11y:
    orientacoes: Sequence[OrientacaoA11y]
    parser_factory: Callable[[str], Parser] = Parser
    localizador: LocalizadorHtml = field(default_factory=LocalizadorHtml)
    fabrica_achado: FabricaAchado = field(default_factory=FabricaAchado)

    def analisar_html(self, html: str) -> list[AchadoA11y]:
        parser = self.parser_factory(html)
        parser.criar_ids()
        achados = []

        for orientacao in self.orientacoes:
            for item in orientacao.rodar(parser):
                achados.append(self.fabrica_achado.criar(item, orientacao))

        return achados

    def analisar_arquivo(self, caminho: str | Path) -> ResultadoArquivo:
        caminho = Path(caminho)
        try:
            html = caminho.read_text(encoding="utf-8")
            return ResultadoArquivo(caminho=caminho, achados=self.analisar_html(html))
        except Exception as erro:  # mantém a análise dos outros arquivos.
            return ResultadoArquivo(caminho=caminho, erro=str(erro))

    def analisar_caminho(self, caminho: str | Path) -> ResultadoAnalise:
        origem = Path(caminho)
        arquivos = self.localizador.encontrar(origem)
        if not arquivos:
            return ResultadoAnalise(origem=origem, erros=[f"Nenhum HTML encontrado em {origem}"])

        resultado = ResultadoAnalise(origem=origem)
        for arquivo in arquivos:
            resultado.arquivos.append(self.analisar_arquivo(arquivo))
        return resultado


def encontrar_arquivos_html(caminho: str | Path) -> list[Path]:
    return LocalizadorHtml().encontrar(caminho)


def analisar_html(html: str, orientacoes: Sequence[OrientacaoA11y]) -> list[AchadoA11y]:
    return AnalisadorA11y(orientacoes).analisar_html(html)


def analisar_arquivo(caminho: str | Path, orientacoes: Sequence[OrientacaoA11y]) -> ResultadoArquivo:
    return AnalisadorA11y(orientacoes).analisar_arquivo(caminho)


def analisar_caminho(caminho: str | Path, orientacoes: Sequence[OrientacaoA11y]) -> ResultadoAnalise:
    return AnalisadorA11y(orientacoes).analisar_caminho(caminho)


def criar_achado(dados, orientacao: OrientacaoA11y) -> AchadoA11y:
    return FabricaAchado().criar(dados, orientacao)
