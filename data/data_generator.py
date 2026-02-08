"""
Módulo para gerar dados de materiais em lotes e salvar em um arquivo JSONL.
Isso ajuda a economizar memória RAM ao evitar o carregamento de todos os dados na memória de uma vez.

"""

from faker import Faker
from models import Materials
import random

fake = Faker()

nomes_possiveis = [
    "Cantoneira",
    "Barra Redonda",
    "Chato Mola",
    "Barra Chata",
    "Perfil I",
    "Perfil H",
    "Perfil U",
]


def generate_and_save_materials_in_batches(
    filename="data/materials_data.jsonl", batch_size=1000, total_records=50000
):
    """
    Gera e salva materiais em um arquivo JSON Lines (JSONL) para economizar RAM.
    Cada linha do arquivo será um objeto JSON independente.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(0, total_records, batch_size):
            # Processa apenas o batch atual na memória
            current_batch_size = min(batch_size, total_records - i)

            for _ in range(current_batch_size):
                material = Materials(
                    material_id=random.randint(1, 1000000),
                    material_name=f"{random.choice(nomes_possiveis)} {round(random.uniform(2.0, 6.5), 2)}mm",
                    ton=round(random.uniform(0.1, 100.0), 2),
                    price=round(random.uniform(2000.0, 10000.0), 2),
                    lat_and_long=[
                        round(random.uniform(-90.0, 90.0), 6),
                        round(random.uniform(-180.0, 180.0), 6),
                    ],
                )
                # Escreve no disco imediatamente e limpa a referência do objeto
                f.write(material.model_dump_json() + "\n")

            print(
                f"Processados {i + current_batch_size} de {total_records} registros..."
            )


if __name__ == "__main__":
    generate_and_save_materials_in_batches()
