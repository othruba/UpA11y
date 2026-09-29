from __future__ import annotations

import argparse

from upa11y.analise.processador import ResultadoAnalise, analisar_caminho
from upa11y.orientacoes import CONJUNTO_VAZIO
from upa11y.orientacoes.serializacao import exportar_conjunto, importar_conjunto


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa verificações de acessibilidade.")
    parser.add_argument("caminho", nargs="?", default="sample")
    parser.add_argument("--orientacoes", help="JSON com testes e refatorações.")
    parser.add_argument("--exportar-orientacoes", help="Caminho para exportar o JSON carregado.")
    args = parser.parse_args()

    conjunto = importar_conjunto(args.orientacoes) if args.orientacoes else CONJUNTO_VAZIO

    if args.exportar_orientacoes:
        destino = exportar_conjunto(conjunto, args.exportar_orientacoes)
        print(f"Orientações exportadas para: {destino}")
        return

    if not conjunto.orientacoes:
        parser.error("Use --orientacoes para informar um JSON de testes.")

    imprimir_resultado(analisar_caminho(args.caminho, conjunto.orientacoes))


def imprimir_resultado(resultado: ResultadoAnalise) -> None:
    print(f"Origem analisada: {resultado.origem}")

    for erro in resultado.erros:
        print(f"Erro: {erro}")
    if resultado.erros:
        return

    contagem = resultado.contagem_severidade
    print(
        f"Resumo: {resultado.arquivos_processados} arquivo(s), "
        f"{resultado.total_achados} achado(s), "
        f"{contagem.get('error', 0)} erro(s), "
        f"{contagem.get('warning', 0)} aviso(s)."
    )

    for arquivo in resultado.arquivos:
        print(f"\n{arquivo.caminho_relativo(resultado.origem)}: {arquivo.total_achados} achado(s)")
        for achado in arquivo.achados:
            print(
                f"- [{achado.severidade}] {achado.recomendacao} "
                f"{achado.elemento}: {achado.problema} "
                f"Sugestao: {achado.sugestao}"
            )


if __name__ == "__main__":
    main()
