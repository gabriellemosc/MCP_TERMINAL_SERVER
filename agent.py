import re
import random
from mcp.client import send_mcp_request, MCPMethod

def parse_number(input_str):
    match = re.search(r'\d+', input_str)
    return int(match.group()) if match else None

def virtual_agent():
    while True:
        saudacoes = [
            "👋 Olá! Sou o Gabriel, seu assistente para encontrar seu carro",
            "E aí! Eu sou o Gabriel, vou te ajudar a achar o carro perfeito!",
            "Oi! Que bom te ver por aqui! Sou o Gabriel, especialista em encontrar carros incríveis!",
            "Olá! Preparado para encontrar seu próximo carro? Sou o Gabriel e vou te ajudar!"
        ]
        print(random.choice(saudacoes))
        print("Vamos conversar sobre o que você tá procurando...\n")
        print("Apenas um aviso: quanto mais informações, mais preciso será o resultado\n")

        filtros = {}

        respostas_marca = [
            "Ok! De qual marca você quer ver? Pode ser Toyota, Honda, Volkswagen etc...",
            "Boa! Qual marca te chama mais atenção? Fiat, Chevrolet, Hyundai etc...",
            "Me conta das marcas que você gosta mais."
        ]
        marca = input(f"{random.choice(respostas_marca)} ").strip()
        if marca:
            filtros['marca'] = marca
            print(f"Marca Selecionada: {marca}!\n")

        if marca:
            respostas_modelo = [
                f"E  da {marca}, tem algum modelo que você gosta mais?",
                f"Certo! Tem algum modelo da {marca} que você prefere?",
                f"Da {marca}, qual modelo te interessa?"
            ]
        else:
            respostas_modelo = [
                "Algum modelo específico?",
                "Qual modelo você tá pensando?"
            ]
        modelo = input(f"{random.choice(respostas_modelo)} ").strip()
        if modelo:
            filtros['modelo'] = modelo
            print(f"💡 {modelo} é um bom carro!\n")

        respostas_ano = [
            "E sobre o ano? Algum ano para poder dizer?",
            "Sobre o ano do carro, você tem preferência? Pode ser uma faixa ou ano específico",
            "E o ano? Pode falar 'mais novo que 2020' ou 'entre 2015 e 2020'..."
        ]
        ano_input = input(f"{random.choice(respostas_ano)} ").strip().lower()
        if ano_input:
            if '-' in ano_input:
                try:
                    ano_min, ano_max = ano_input.split('-')
                    filtros['ano_min'] = parse_number(ano_min)
                    filtros['ano_max'] = parse_number(ano_max)
                    print(f"📅 Entendi! Entre {filtros['ano_min']} e {filtros['ano_max']}\n")
                except:
                    print("Não foi possível entender os anos.\n")
            elif any(p in ano_input for p in ['novo', 'recente', 'atual']):
                filtros['ano_min'] = 2020
                print("Beleza. Vou focar nos mais novos 🚗\n")
            elif any(p in ano_input for p in ['antigo', 'clássico', 'vintage']):
                filtros['ano_max'] = 2010
                print("Carro mais antigo? Boa escolha 😎\n")
            else:
                ano = parse_number(ano_input)
                if ano:
                    filtros['ano_min'] = ano
                    print(f"✅ Certo! A partir de {ano}\n")

        respostas_combustivel = [
            "E o combustível? Tem preferência ou tá de boa com qualquer um?",
            "Falando em abastecer, qual combustível você prefere?",
            "Sobre o tanque: gasolina, álcool, flex... qual é seu preferido?",
            "E na hora de abastecer, você é mais de qual tipo?"
        ]
        combustivel = input(f"{random.choice(respostas_combustivel)} ").strip()
        if combustivel:
            if 'flex' in combustivel.lower():
                filtros['tp_combustivel'] = 'Flex'
                print("Flex? Boa escolha 🔁\n")
            elif 'gasolina' in combustivel.lower():
                filtros['tp_combustivel'] = 'Gasolina'
                print("Gasolina é uma boa escolha ⛽\n")
            elif any(p in combustivel.lower() for p in ['álcool', 'alcool', 'etanol']):
                filtros['tp_combustivel'] = 'Etanol'
                print("Etanol, econômico 💨\n")
            else:
                filtros['tp_combustivel'] = combustivel
                print(f"Procurar por {combustivel}\n")

        respostas_preco = [
            "Agora falando do investimento. Qual seria sua faixa de preço?",
            "E o orçamento? Pode falar valores aproximados.",
            "Falando em dinheiro, quanto você tá pensando em investir?"
        ]
        preco_input = input(f"{random.choice(respostas_preco)} ").strip()
        if preco_input:
            if '-' in preco_input:
                try:
                    preco_min, preco_max = preco_input.split('-')
                    filtros['preco_min'] = parse_number(preco_min)
                    filtros['preco_max'] = parse_number(preco_max)
                    print(f"Beleza, entre R$ {filtros['preco_min']:,} e R$ {filtros['preco_max']:,}\n")
                except:
                    print("Valores confusos, mas vou pesquisar mesmo assim!\n")
            elif any(p in preco_input.lower() for p in ['barato', 'econômico', 'até']):
                preco = parse_number(preco_input)
                if preco:
                    filtros['preco_max'] = preco
                    print(f"Entendido! Até R$ {preco:,}\n")
            else:
                preco = parse_number(preco_input)
                if preco:
                    filtros['preco_max'] = preco
                    print(f"Show! Até R$ {preco:,}\n")

        mensagens_busca = [
            "\n🔎 Certo, deixe eu dar uma olhada aqui no que temos.",
            "\n🔎 Beleza! Vou procurar no banco de dados pra achar suas opções.",
            "\n🔎 Deixa eu consultar nosso sistema pra encontrar as opções..."
        ]
        print(random.choice(mensagens_busca))
        print("Pode demorar um pouquinho, estou buscando...\n")

        response = send_mcp_request(MCPMethod.SEARCH_VEHICLES, filtros)

        if response.get("result") and "results" in response["result"]:
            results = response["result"]["results"]
            if results:
                mensagens_sucesso = [
                    f"{len(results)} resultados encontrados com base nas suas respostas!",
                    f"✅ Achei {len(results)} carros que podem te agradar.",
                    f"Boas notícias! Tenho {len(results)} opções pra você.",
                    f"💫 Muito bem! Encontrei {len(results)} carros que podem te satisfazer."
                ]
                print(random.choice(mensagens_sucesso))
                print()
                for i, v in enumerate(results, 1):
                    status = "🟢" if v['disponivel'] else "🔴"
                    print(f"{i}. {status} {v['marca']} {v['modelo']} ({v['ano']})")
                    print(f"     {v['cor']} | 📊 {v['quilometragem']:,} km")
                    print(f"     ⚙️ Transmissão: {v['tp_transmissao']} | ⛽ {v['tp_combustivel']}")
                    print(f"     💰 R$ {v['preco']:,.2f}")
                    if v['disponivel']:
                        print("    ✅ Disponível pra test-drive!")
                    else:
                        print("    ⏳ Já foi vendido, mas posso procurar outros similares!")
                    print()
            else:
                print("📝 Nenhum carro encontrado com essas características.\n")
        else:
            erro = response.get('error', 'Resposta inválida do servidor')
            print(f"❌ Ocorreu um problema: {erro}\nTenta de novo em alguns minutos!\n")

        sair = input("🔁 Deseja fazer uma nova busca? (s/n): ").strip().lower()
        if sair == 'n':
            despedidas = [
                "\n👋 Volte sempre!",
                "\n Espero que encontre o carro! Até mais!",
                "\n Obrigado. Boa sorte na busca!"
            ]
            print(random.choice(despedidas))
            break

if __name__ == "__main__":
    virtual_agent()
