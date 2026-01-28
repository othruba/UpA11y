from orientacoes.orientacao import OrientacaoA11y

def img_tem_alt(tag):
    return tag.has_attr("alt") and tag["alt"].strip() != ""

def add_alt_generico(tag):
    tag["alt"] = "Adicione uma descrição textual para este conteúdo"

ori19 = OrientacaoA11y(
    num_orientacao="19",
    descricao="Vídeos e imagens devem apresentar uma descrição textual.",
    tags_alvo=["img"],
    teste=img_tem_alt,
    refatoracao=add_alt_generico
)

ORIENTACOES = [ori19]