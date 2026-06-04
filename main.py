from flask import Flask, render_template, request, redirect, url_for

import times
import partidas
import torneios
import ranking

app = Flask(__name__)

lista_partidas = []
confrontos_atuais = []
resultados_rodada_atual = []
campeao = None
numero_rodada = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/times")
def pagina_times():
    todos_times = times.listar_times()
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    busca_id = request.args.get("busca_id", "").strip()
    resultado_busca = None
    if busca_id:
        resultado_busca = times.buscar_time(busca_id)
    return render_template("times.html", times=todos_times, msg=msg, tipo=tipo,
                           busca_id=busca_id, resultado_busca=resultado_busca)


@app.route("/times/criar", methods=["POST"])
def criar_time():
    nome = request.form.get("nome", "").strip()
    jogadores_raw = request.form.get("jogadores", "").strip()
    jogadores = [j.strip() for j in jogadores_raw.split(",") if j.strip()] if jogadores_raw else []
    resultado = times.criar_time(nome, jogadores)
    if isinstance(resultado, dict):
        return redirect(url_for("pagina_times", msg=f"Time '{resultado['nome']}' criado com sucesso.", tipo="sucesso"))
    return redirect(url_for("pagina_times", msg=resultado, tipo="erro"))


@app.route("/times/remover/<identificador>")
def remover_time(identificador):
    resultado = times.remover_time(identificador)
    if resultado.startswith("Erro"):
        return redirect(url_for("pagina_times", msg=resultado, tipo="erro"))
    return redirect(url_for("pagina_times", msg=resultado, tipo="sucesso"))


@app.route("/partidas")
def pagina_partidas():
    todos_times = times.listar_times()
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    filtro_time = request.args.get("filtro_time", "").strip()
    filtro_rodada = request.args.get("filtro_rodada", "").strip()

    partidas_filtradas = list(lista_partidas)
    if filtro_time:
        partidas_filtradas = [
            p for p in partidas_filtradas
            if p.get("time1", "").lower() == filtro_time.lower()
            or p.get("time2", "").lower() == filtro_time.lower()
        ]
    if filtro_rodada:
        partidas_filtradas = [
            p for p in partidas_filtradas
            if str(p.get("rodada", "")) == filtro_rodada
        ]

    rodadas = sorted({str(p.get("rodada", "")) for p in lista_partidas if p.get("rodada")})

    return render_template(
        "partidas.html",
        partidas=partidas_filtradas,
        todos_times=todos_times,
        rodadas=rodadas,
        filtro_time=filtro_time,
        filtro_rodada=filtro_rodada,
        msg=msg,
        tipo=tipo,
    )


@app.route("/partidas/registrar", methods=["POST"])
def registrar_partida():
    time1 = request.form.get("time1", "").strip()
    time2 = request.form.get("time2", "").strip()
    gols1 = int(request.form.get("gols_time1", 0))
    gols2 = int(request.form.get("gols_time2", 0))
    resultado = partidas.registrar_resultado(lista_partidas, time1, time2, gols1, gols2)
    if isinstance(resultado, dict) and "erro" in resultado:
        return redirect(url_for("pagina_partidas", msg=resultado["erro"], tipo="erro"))
    if isinstance(resultado, dict):
        ranking.atualizar_pontos(resultado)
        return redirect(url_for("pagina_partidas", msg="Partida registrada com sucesso.", tipo="sucesso"))
    return redirect(url_for("pagina_partidas", msg=str(resultado), tipo="erro"))


@app.route("/torneio")
def pagina_torneio():
    todos_times = times.listar_times()
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    return render_template(
        "torneio.html",
        times=todos_times,
        confrontos=confrontos_atuais,
        resultados=resultados_rodada_atual,
        campeao=campeao,
        msg=msg,
        tipo=tipo,
    )


@app.route("/torneio/gerar", methods=["POST"])
def gerar_confrontos():
    global confrontos_atuais, resultados_rodada_atual, campeao
    todos_times = times.listar_times()
    if len(todos_times) < 2:
        return redirect(url_for("pagina_torneio", msg="É necessário pelo menos 2 times para gerar confrontos.", tipo="erro"))
    nomes = [t["nome"] for t in todos_times]
    ranking.criar_tabela(nomes) 
    confrontos_atuais = torneios.gerar_confronto(nomes)
    resultados_rodada_atual = []
    campeao = None
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/iniciar", methods=["POST"])
def iniciar_rodada():
    global lista_partidas, resultados_rodada_atual, numero_rodada
    numero_rodada += 1
    resultados_rodada_atual = torneios.iniciar_rodada(confrontos_atuais)
    for resultado in resultados_rodada_atual:
        resultado["rodada"] = numero_rodada
        lista_partidas.append(resultado)
        ranking.atualizar_pontos(resultado)
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/avancar", methods=["POST"])
def avancar_fase():
    global confrontos_atuais, resultados_rodada_atual, campeao
    classificados = torneios.avancar_fase(resultados_rodada_atual)
    if len(classificados) == 1:
        campeao = classificados[0]
        confrontos_atuais = []
        resultados_rodada_atual = []
    else:
        confrontos_atuais = torneios.gerar_confronto(classificados)
        resultados_rodada_atual = []
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/reiniciar", methods=["POST"])
def reiniciar_torneio():
    global lista_partidas, confrontos_atuais, resultados_rodada_atual, campeao, numero_rodada
    lista_partidas = []
    confrontos_atuais = []
    resultados_rodada_atual = []
    campeao = None
    numero_rodada = 0
    nomes = [t["nome"] for t in times.listar_times()]
    ranking.criar_tabela(nomes)
    return redirect(url_for("pagina_torneio"))


@app.route("/ranking")
def pagina_ranking():
    classificacao = ranking.ordenar_classificacao()
    return render_template("ranking.html", classificacao=classificacao)


if __name__ == "__main__":
    app.run(debug=True)
