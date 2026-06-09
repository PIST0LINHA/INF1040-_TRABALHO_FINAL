from unittest.mock import patch
import partidas

erros = []
total = 0
sucesso = 0


def checar(nome_teste, obtido, esperado):
    global total, sucesso
    total += 1
    if obtido == esperado:
        sucesso += 1
    else:
        erros.append(
            f"{nome_teste}: esperado {esperado!r}, obtido {obtido!r}"
        )  # !r trata string como string literal


# --------- simular_partida

# Caso 1: O mesmo time é inserido duas vezes

partidas._lista_partidas = []
resultado = partidas.simular_partida("Vasco", "Vasco")
checar(
    "simular partida | mesmo time",
    resultado.get("erro"),
    "Erro: um time não pode disputar contra si mesmo",
)

# Caso 2: Função é chamada com apenas um time

partidas._lista_partidas = []
resultado = partidas.simular_partida("Vasco", "")
checar(
    "simular partida | time vazio",
    resultado.get("erro"),
    "Erro: nomes dos times não podem ser vazios",
)

# Caso 3: Função é chamada corretamente

partidas._lista_partidas = []
with patch("partidas.random.randint", side_effect=[3, 5]):
    resultado = partidas.simular_partida("Vasco", "Flamengo")
    checar(
        "simular partida | chamada válida",
        resultado,
        {"time1": "Vasco", "time2": "Botafogo", "gols_time1": 3, "gols_time2": 5},
    )

# --------- gerar_resultado

# Caso 1: partida com erro
partidas._lista_partidas = []
partida_erro = partidas.simular_partida("Vasco", "")
resultado = partidas.gerar_resultado(partida_erro)
checar(
    "gerar_resultado | partida com erro",
    resultado,
    "Erro: nomes dos times não podem ser vazios",
)

# Caso 2: partida válida
partidas._lista_partidas = []
with patch("partidas.random.randint", side_effect=[3, 5]):
    partida_valida = partidas.simular_partida("Vasco", "Botafogo")
resultado = partidas.gerar_resultado(partida_valida)
checar(
    "gerar_resultado | partida válida",
    resultado,
    "Vasco:3  xBotafogo: 5",
)

# --------- registrar_resultado

# Caso 1: mesmo time
partidas._lista_partidas = []
lista = []
resultado = partidas.registrar_resultado(lista, "Vasco", "Vasco", 3, 5)
checar(
    "registrar_resultado | mesmo time",
    resultado.get("erro"),
    "Erro: um time não pode disputar contra si mesmo",
)

# Caso 2: time vazio
partidas._lista_partidas = []
lista = []
resultado = partidas.registrar_resultado(lista, "Vasco", "", 3, 5)
checar(
    "registrar_resultado | time vazio",
    resultado.get("erro"),
    "Erro: nomes dos times não podem ser vazios",
)

# Caso 3: chamada válida
partidas._lista_partidas = []
lista = []
resultado = partidas.registrar_resultado(lista, "Vasco", "Botafogo", 3, 5)
checar(
    "registrar_resultado | chamada válida",
    resultado,
    {"time1": "Vasco", "time2": "Botafogo", "gols_time1": 3, "gols_time2": 5},
)

# --------- listar_partidas

# Caso 1: lista com partidas
lista = [{"time1": "Vasco", "time2": "Botafogo", "gols_time1": 2, "gols_time2": 1}]
resultado = partidas.listar_partidas(lista)
checar(
    "listar_partidas | lista com partidas",
    resultado,
    [{"time1": "Vasco", "time2": "Botafogo", "gols_time1": 2, "gols_time2": 1}],
)

# Caso 2: lista vazia
resultado = partidas.listar_partidas([])
checar(
    "listar_partidas | lista vazia",
    resultado,
    [],
)

# --------- relatório

print(f"\n{total} testes realizados")
print(f"{sucesso} testes com sucesso")
print(f"{total - sucesso} com erros")

if erros:
    print("\nErros:")
    for e in erros:
        print(f"  - {e}")
