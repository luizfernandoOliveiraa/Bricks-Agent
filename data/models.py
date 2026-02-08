"""
Nessa classe são definidos os modelos utilizados pelo faker para gerar os dados.
Utilizamos o Pydantic para garantir a validação e estrutura dos dados gerados.
"""

from pydantic import BaseModel


class Materials(BaseModel):
    """
    O bom uso do Pydantic ajuda a garantir que os dados gerados estejam
    sempre no formato correto, facilitando a manipulação e armazenamento posterior.
    """

    material_id: int
    material_name: str
    ton: float
    price: float
    lat_and_long: list[float]
