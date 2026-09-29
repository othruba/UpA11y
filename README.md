# UpA11y

Ferramenta desktop e de linha de comando para analisar acessibilidade em arquivos HTML estáticos.

## Requisitos

- Python 3.10 ou superior;
- `pip` ou [uv](https://docs.astral.sh/uv/);
- ambiente gráfico para abrir a interface PyQt.

Funciona em Windows, macOS e Linux. A análise pela linha de comando não exige interface gráfica.

## Instalação

No diretório do projeto, crie e ative um ambiente virtual.

| Sistema | Criar ambiente | Ativar ambiente |
| --- | --- | --- |
| Windows (PowerShell) | `py -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `py -m venv .venv` | `.venv\Scripts\activate.bat` |
| macOS/Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |

Em seguida, instale o projeto:

```bash
python -m pip install --upgrade pip
python -m pip install .
```

Com `uv`, a alternativa mais curta é:

```bash
uv sync
```

## Uso

Após instalar com `pip`, abra a interface com:

```bash
upa11y-gui
```

Ou execute sem instalar comandos globais:

```bash
python -m upa11y.interface.main
```

Na interface, importe um JSON na tela inicial ou na aba **Editor**. Ali é possível selecionar testes e refatorações, editar seus metadados e código, salvar a edição e exportar o conjunto.

Para analisar uma pasta ou arquivo HTML pela linha de comando:

```bash
upa11y sample --orientacoes exports/orientacoes-upa11y.json
```

Sem os comandos instalados, use:

```bash
python -m upa11y.cli sample --orientacoes exports/orientacoes-upa11y.json
```

Para exportar uma cópia de um conjunto de orientações:

```bash
upa11y --orientacoes exports/orientacoes-upa11y.json --exportar-orientacoes exports/copia-orientacoes.json
```

## Estrutura

- `upa11y/analise`: localiza e processa arquivos HTML.
- `upa11y/orientacoes`: carrega, executa e exporta orientações.
- `upa11y/interface`: interface gráfica em PyQt.
- `upa11y/parser`: acesso ao documento HTML.
- `exports/`: conjunto de orientações de exemplo.
- `sample/`: página HTML de exemplo.
- `docs/`: diagramas e materiais de referência.

## Formato das orientações

O arquivo de orientações é JSON e tem este formato:

```json
{
  "formato": "upa11y.orientacoes.codigo",
  "versao": 2,
  "titulo": "Meu conjunto",
  "utils": "def achado(...): ...",
  "orientacoes": [
    {
      "num_orientacao": "REC1",
      "descricao": "Descrição da regra.",
      "funcao": "testar",
      "codigo": "def testar(analisador):\\n    return []",
      "refatoracoes": [
        {
          "titulo": "Refatoração exemplo",
          "descricao": "Descrição da ação.",
          "funcao": "refatorar",
          "codigo": "def refatorar(documento, achado=None):\\n    return documento"
        }
      ]
    }
  ]
}
```

O código em `utils` é executado antes dos testes e fica disponível para todos eles. Cada item em `orientacoes` deve declarar a função de teste em `funcao`.
Cada teste pode declarar zero, uma ou várias `refatoracoes`; elas aparecem como filhos do teste na árvore, mas ainda não são executadas automaticamente.

> Atenção: os campos `utils`, `codigo` e `codigo` de refatorações contêm código Python executável. Importe apenas arquivos de fontes confiáveis.

## Observações por sistema

- **Windows:** caso o PowerShell bloqueie a ativação do ambiente virtual, use o Prompt de Comando ou execute os comandos com `py` sem ativar o ambiente.
- **macOS:** se o sistema perguntar sobre a execução do aplicativo, permita a abertura nas configurações de privacidade e segurança.
- **Linux:** em sessões sem interface gráfica (por exemplo, servidores), use a CLI. Em desktops, instale os componentes gráficos indicados pela sua distribuição caso o Qt solicite dependências do sistema.
