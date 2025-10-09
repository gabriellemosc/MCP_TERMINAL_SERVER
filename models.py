#define a tabela de veículos e helpers
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean, Index, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()

class Veiculos(Base):
    __tablename__ = "carros"

    # atributos principais carro
    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    # Busca e Filtro
    motorizacao = Column(String(50))
    tp_combustivel = Column(String(20)) 
    tp_transmissao = Column(String(20))     #manual || automatico
    num_portas = Column(Integer)
    modelo_carro = Column(String(30))      #  Sedan, Hatch etc...

    #status e visualizacao
    cor = Column(String(30))
    quilometragem = Column(Integer)
    preco = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True) # Disponível para venda


      
    def __repr__(self):
        return f"<Carro - marca='{self.marca}' -  modelo='{self.modelo}' - ano={self.ano} -  preco={self.preco})>"
    

#criar BD
engine = create_engine('sqlite:///inventario.db') 
if __name__ == "__main__":
    Base.metadata.create_all(engine)

logging.info("BD criado!")