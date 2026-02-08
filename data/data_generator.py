import random
import json
from models import Materials

# Dicionário expandido para garantir variabilidade semântica no RAG
CONTEUDO_RAG = {
    "Cantoneira": {
        "verbos": ["Indicada para", "Utilizada em", "Essencial para", "Aplicada em"],
        "adjetivos": [
            "estruturas metálicas leves",
            "torres de transmissão",
            "serralheria industrial",
            "suportes reforçados",
        ],
        "detalhes": [
            "alta resistência à flexão",
            "facilidade de soldagem",
            "acabamento galvanizado disponível",
        ],
    },
    "Barra Redonda": {
        "verbos": ["Ideal para", "Destinada a", "Muito comum em", "Uso focado em"],
        "adjetivos": [
            "fabricação de eixos",
            "grades de proteção",
            "trefilação de precisão",
            "usinagem de peças",
        ],
        "detalhes": [
            "superfície lisa e uniforme",
            "excelente forjabilidade",
            "precisão dimensional",
        ],
    },
    "Chato Mola": {
        "verbos": [
            "Desenvolvida para",
            "Exclusiva para",
            "Projetada para",
            "Empregada em",
        ],
        "adjetivos": [
            "feixes de molas",
            "sistemas de suspensão",
            "componentes automotivos",
            "implementos de amortecimento",
        ],
        "detalhes": [
            "alto teor de carbono",
            "elasticidade controlada",
            "resistência à fadiga mecânica",
        ],
    },
    "Barra Chata": {
        "verbos": [
            "Recomendada para",
            "Largamente usada em",
            "Base para",
            "Funcional em",
        ],
        "adjetivos": [
            "grades e portões",
            "esquadrias metálicas",
            "reforços de estruturas",
            "trilhos leves",
        ],
        "detalhes": [
            "versatilidade de corte",
            "ampla gama de espessuras",
            "fácil conformação",
        ],
    },
    "Perfil I": {
        "verbos": [
            "Suporte para",
            "Viga mestra em",
            "Elemento de",
            "Base de sustentação para",
        ],
        "adjetivos": [
            "edifícios de múltiplos andares",
            "pontes rolantes",
            "galpões industriais",
            "grandes vãos livres",
        ],
        "detalhes": [
            "formato eficiente para cargas",
            "estabilidade estrutural",
            "normas ASTM rigorosas",
        ],
    },
    "Perfil H": {
        "verbos": [
            "Pilar de",
            "Robusta solução para",
            "Elemento crítico em",
            "Suporte pesado para",
        ],
        "adjetivos": [
            "fundações profundas",
            "colunas de sustentação",
            "obras de grande porte",
            "viadutos",
        ],
        "detalhes": [
            "máxima rigidez",
            "resistência à compressão",
            "ideal para projetos pesados",
        ],
    },
    "Perfil U": {
        "verbos": ["Estrutura de", "Componente para", "Versátil em", "Utilizado em"],
        "adjetivos": [
            "chassis de veículos",
            "implementos agrícolas",
            "coberturas metálicas",
            "estruturas secundárias",
        ],
        "detalhes": [
            "bom momento de inércia",
            "facilidade de encaixe",
            "ótima relação peso-resistência",
        ],
    },
}


def gerar_descricao_rag(material_base, medida):
    """Gera uma descrição única para evitar colapso de embeddings no RAG."""
    info = CONTEUDO_RAG[material_base]
    verbo = random.choice(info["verbos"])
    adjetivo = random.choice(info["adjetivos"])
    detalhe = random.choice(info["detalhes"])

    # A inclusão da medida no texto ajuda o retriever a encontrar o item correto por busca semântica
    return f"{verbo} {adjetivo}. Este item possui {detalhe}. Especificação técnica: bitola de {medida}mm."


def generate_and_save_materials_in_batches(
    filename="materials_data.jsonl", batch_size=1000, total_records=55000
):
    """Gera dados em lotes para economizar RAM e salvar em formato JSONL."""
    nomes_possiveis = list(CONTEUDO_RAG.keys())

    print(f"🛠️  Gerando base de conhecimento para RAG com {total_records} registros...")

    with open(filename, "w", encoding="utf-8") as f:
        for i in range(0, total_records, batch_size):
            current_batch_size = min(batch_size, total_records - i)

            for _ in range(current_batch_size):
                base_name = random.choice(nomes_possiveis)
                medida = round(
                    random.uniform(1.5, 75.0), 2
                )  # Range aumentado para maior diversidade

                material = Materials(
                    material_id=random.randint(1000000, 9999999),
                    material_name=f"{base_name} {medida}mm",
                    ton=round(random.uniform(0.1, 500.0), 3),
                    price=round(random.uniform(3000.0, 15000.0), 2),
                    description=gerar_descricao_rag(base_name, medida),
                )

                # model_dump_json() é ideal para Pydantic v2
                f.write(material.model_dump_json() + "\n")

            print(
                f"📦 Progresso: {i + current_batch_size}/{total_records} itens processados."
            )

    print(
        f"\n✅ Concluído! Arquivo '{filename}' pronto para ingestão no banco de vetores."
    )


if __name__ == "__main__":
    generate_and_save_materials_in_batches()
