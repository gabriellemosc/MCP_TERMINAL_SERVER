"""
Tipos de mensagens e estruturas de dados do protocolo MCP
para o domínio de veículos.
"""

from pydantic import BaseModel, Field
from pydantic import validator
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

#import data from popular_bd.py
try:
    from popular_bd import (
        cores,
        combustiveis,
        transmissoes,
        categorias,
         modelos_por_marca,
        categoria_por_modelo
    )

      # Cria enums baseados nos dados reais
    Cores = Enum('Cores', {cor.upper(): cor for cor in cores})
    TipoCombustivel = Enum('TipoCombustivel', {comb.upper(): comb for comb in combustiveis})
    TipoTransmissao = Enum('TipoTransmissao', {trans.upper(): trans for trans in transmissoes})
    ModeloCarro = Enum('ModeloCarro', {cat.upper(): cat for cat in categorias})

    MARCAS_DISPONIVEIS = list(modelos_por_marca.keys())
    MODELOS_POR_MARCA = modelos_por_marca
    CATEGORIA_POR_MODELO = categoria_por_modelo

except ImportError as e:
    print(f"Não foi possivel importar {e}")

    #Definir todas as variáveis necessárias
    cores = ["Branco", "Preto", "Prata", "Cinza", "Vermelho", "Azul", "Verde"]
    combustiveis = ["Gasolina", "Etanol", "Flex"]
    transmissoes = ["Manual", "Automática"]
    categorias = ["Hatch", "Sedan", "SUV", "Picape", "Conversível"]

    modelos_por_marca = {
        "Fiat": ["Uno", "Fiorino"],
        "Volkswagen": ["Golf", "Jetta", "Polo"],
        "Chevrolet": ["Cruze", "Onix", "Camaro"],
        "Toyota": ["Corolla", "Supra", "Hilux"],
        "Hyundai": ["HB20", "i30", "Tucson"],
        "Honda": ["Civic", "Fit", "Accord"],
        "Renault": ["Sandero", "Duster"],
        "Ford": ["Fiesta", "Focus", "Ranger"],
        "Jeep": ["Renegade", "Wrangler", "Compass"],
        "Nissan": ["Sentra", "Frontier", "Leaf"]
    }

    categoria_por_modelo = {
        "Uno": "Hatch", "Fiorino": "Picape",
        "Golf": "Hatch", "Jetta": "Sedan", "Polo": "Hatch",
        "Cruze": "Sedan", "Onix": "Hatch", "Camaro": "Conversível",
        "Corolla": "Sedan", "Supra": "Conversível", "Hilux": "Picape",
        "HB20": "Hatch", "i30": "Hatch", "Tucson": "SUV",
        "Civic": "Sedan", "Fit": "Hatch", "Accord": "Sedan",
        "Sandero": "Hatch", "Duster": "SUV",
        "Fiesta": "Hatch", "Focus": "Hatch", "Ranger": "Picape",
        "Renegade": "SUV", "Wrangler": "SUV", "Compass": "SUV",
        "Sentra": "Sedan", "Frontier": "Picape", "Leaf": "Hatch"
    }

    #create the datas from the file itself
     # Create ENUMS

    Cores = Enum('Cores', {cor.upper(): cor for cor in cores})
    TipoCombustivel = Enum('TipoCombustivel', {c.upper(): c for c in combustiveis})
    TipoTransmissao = Enum('TipoTransmissao', {t.upper(): t for t in transmissoes})
    ModeloCarro = Enum('ModeloCarro', {cat.upper(): cat for cat in categorias})

 
    MARCAS_DISPONIVEIS = list(modelos_por_marca.keys())
    MODELOS_POR_MARCA = modelos_por_marca
    CATEGORIA_POR_MODELO = categoria_por_modelo

   

  
#MESSAGE STRUCT

class VehicleSearchRequest(BaseModel):
     marca: Optional[str] = Field(None, description="Marca do veículo")
     modelo: Optional[str] = Field(None, description="Modelo do veículo")
     ano_min: Optional[int] = Field(None, ge=1990, le=2025)
     ano_max: Optional[int] = Field(None, ge=1990, le=2025)
     
     tp_combustivel: Optional[str] = Field(None, description="Tipo de combustível")  

     tp_transmissao: Optional[str] = Field(None, description="Tipo de transmissão")
     preco_min: Optional[float] = Field(None, ge=0)
     preco_max: Optional[float] = Field(None, ge=0)
     cor: Optional[str] = Field(None, description="Cor do veículo")
     modelo_carro: Optional[str] = Field(None, description="Categoria do veículo")
     disponivel: Optional[bool] = Field(True, description="Apenas veículos disponíveis")

     class Config:
        schema_extra = {
            "example": {
                "marca": "Toyota",
                "ano_min": 2020,
                "preco_max": 80000
            }
        }

#REPRESENT A CAR SEND BY SERVER
class VehicleResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    motorizacao: str
    tp_combustivel: str
    tp_transmissao: str
    num_portas: int
    modelo_carro: str
    cor: str
    quilometragem: int
    preco: float
    disponivel: bool
    descricao: Optional[str] = None

    class Config:
        from_attributes = True  # compatibily wh SQLAlchemy


#REPONSE OF SEARCH SEND BY SERVER
class VehicleSearchResponse(BaseModel):
    success: bool
    message: str
    results: List[VehicleResponse]
    total: int
    filters_applied: Dict[str, Any]
    search_id: str

#MESSAGE STATUS OF SERVER
class HealthResponse(BaseModel):
    status: str
    total_vehicles: int
    available_vehicles: int
    server_version: str = "1.0.0"


#FILTERS AVAILABLE FROM THE CLIENT
class AvailableFilters(BaseModel):
    marcas: List[str] = Field(default_factory=lambda: MARCAS_DISPONIVEIS)
    combustiveis: List[str] = Field(default_factory=lambda: [e.value for e in TipoCombustivel])
    transmissoes: List[str] = Field(default_factory=lambda: [e.value for e in TipoTransmissao])
    cores: List[str] = Field(default_factory=lambda: [e.value for e in Cores])
    tipos_carro: List[str] = Field(default_factory=lambda: [e.value for e in ModeloCarro])
    ano_min: int = 2005
    ano_max: int = 2025
    preco_min: float = 30000.0  
    preco_max: float = 300000.0

def validate_filters(filtros: VehicleSearchRequest) -> List[str]:
    errors = []

    if filtros.ano_min and filtros.ano_max and filtros.ano_min > filtros.ano_max:
      errors.append("Ano mínimo não pode ser maior que ano máximo")
    
    if filtros.preco_min and filtros.preco_max and filtros.preco_min > filtros.preco_max:
         errors.append("Preço mínimo não pode ser maior que preço máximo")
    
    return errors

if __name__ == "__main__":
    # Teste rápido
    print("✅ message_types.py carregado com sucesso!")
    print(f"Marcas: {MARCAS_DISPONIVEIS}")