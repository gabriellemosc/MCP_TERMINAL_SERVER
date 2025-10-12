from models import Base, Veiculos, engine

import logging  #debugger
import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session  #criar sessão

# --- Conectar ao banco DB existente 
engine = create_engine("sqlite:///inventario.db")
Base.metadata.create_all(engine)

# --- Sessão ---
session = Session(engine)


faker = Faker("pt_BR")

#atributos
cores = ["Branco", "Preto", "Prata", "Cinza", "Vermelho", "Azul", "Verde"]
combustiveis = ["Gasolina", "Etanol", "Flex"]
transmissoes = ["Manual", "Automática"]
categorias = ["Hatch", "Sedan", "SUV", "Picape", "Conversível"]

# para seus modelos terem suas respectivas marcas de acordo e NAO CIVIC - Toyota por exemplo
modelos_por_marca = {
    "Fiat": ["Uno", "Fiorino"], "Volkswagen": ["Golf", "Jetta", "Polo"],"Chevrolet": ["Cruze", "Onix", "Camaro"], "Toyota": ["Corolla", "Supra", "Hilux"], "Hyundai": ["HB20", "i30", "Tucson"],
        "Honda": ["Civic", "Fit", "Accord"],
        "Renault": ["Sandero", "Duster"],
        "Ford": ["Fiesta", "Focus", "Ranger"],
        "Jeep": ["Renegade", "Wrangler", "Compass"],
        "Nissan": ["Sentra", "Frontier", "Leaf"]
}


#lógica que cada carro deve estar em sua cateogria respectiva Sandero - HATCH, COROLLA - SEDAN

categoria_por_modelo = {
    "Uno": "Hatch",
    "Fiorino": "Picape",
    "Golf": "Hatch",
    "Jetta": "Sedan",
    "Polo": "Hatch",
      "Cruze": "Sedan",
    "Onix": "Hatch",
    "Camaro": "Conversível",
    "Corolla": "Sedan",
    "Supra": "Conversível",
    "Hilux": "Picape",
    "HB20": "Hatch",
    "i30": "Hatch",
    "Tucson": "SUV",
    "Civic": "Sedan",
    "Fit": "Hatch",
    "Accord": "Sedan",
    "Sandero": "Hatch",
    "Duster": "SUV",
    "Fiesta": "Hatch",
    "Focus": "Hatch",
    "Ranger": "Picape",
    "Renegade": "SUV",
    "Wrangler": "SUV",
    "Compass": "SUV",
    "Sentra": "Sedan",
    "Frontier": "Picape",
    "Leaf": "Hatch"
}


def alimentar_banco(quantidade=100):
    logging.info(f"Inicicando alimentação do BD, com {quantidade}de veículos fictícicos")
    
    veiculos = []

    for _ in range(quantidade):
        marca = random.choice(list(modelos_por_marca.keys()))
        modelo = random.choice(modelos_por_marca[marca])  
        modelo_carro = categoria_por_modelo[modelo]

        ano = random.randint(2005, 2025)
        motorizacao = f"{random.randint(1, 3)}.{random.choice(['0', '6', '8'])}" #ira criar valores padrões de motor como 1.0, 1.6, 2.0 e etc...
        tp_combustivel = random.choice(combustiveis)
        tp_transmissao = random.choice(transmissoes)
        num_portas = random.choice([2, 4])
        cor = random.choice(cores)
        quilometragem = random.randint(1000, 500_000) #carros de 1000km até meio milhao 
        preco = round(random.uniform(30000, 250000), 2)
        disponivel = random.choice([True, True, True, False])  # 75% chance de disponível

        veiculo = Veiculos(
            marca=marca,
            modelo=modelo,
            ano=ano,
            motorizacao=motorizacao,
            tp_combustivel=tp_combustivel,
            tp_transmissao=tp_transmissao,
            num_portas=num_portas,
            modelo_carro=modelo_carro,
            cor=cor,
            quilometragem=quilometragem,
            preco=preco,
            disponivel=disponivel,
            )

        veiculos.append(veiculo)
    
    #adicionar novos values ao BD
    session.add_all(veiculos)
    session.commit()
    session.close()

    logging.info(f"Inseridos {len(veiculos)} ao BD")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  
    alimentar_banco(quantidade=100)         
