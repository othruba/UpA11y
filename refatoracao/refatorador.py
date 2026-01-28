class Refatorador:
    def __init__(self, orientacoes):
        self.orientacoes = orientacoes
        self.problemas = []

    def rodar(self, elementos):
        for orientacao in self.orientacoes:
            for elemento in elementos:
                if elemento.name in orientacao.tags_alvo:
                    passou = orientacao.teste(elemento)
                    if not passou:
                        self.problemas.append({
                            "orientacao": orientacao.num_orientacao,
                            "descricao": orientacao.descricao,
                            "elemento": elemento.name,
                            "elemento_id": elemento.get("upa11y-id"),
                        })
                        if orientacao.refatoracao:
                            orientacao.refatoracao(elemento)

        return self.problemas