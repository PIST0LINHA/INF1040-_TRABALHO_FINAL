from flask import Flask, render_template, request, redirect, url_for

import times
import partidas
import torneios
import ranking

app = Flask(__name__)

lista_partidas = []
tabela_ranking = []
confrontos_atuais = []


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
    return render_template("partidas.html", partidas=lista_partidas)


@app.route("/partidas/registrar", methods=["POST"])
def registrar_partida():
    time1 = request.form.get("time1", "").strip()
    time2 = request.form.get("time2", "").strip()
    gols1 = int(request.form.get("gols_time1", 0))
    gols2 = int(request.form.get("gols_time2", 0))
    partidas.registrar_resultado(lista_partidas, time1, time2, gols1, gols2)
    return redirect(url_for("pagina_partidas"))


@app.route("/torneio")
def pagina_torneio():
    todos_times = times.listar_times()
    return render_template("torneio.html", times=todos_times, confrontos=confrontos_atuais)


@app.route("/torneio/gerar", methods=["POST"])
def gerar_confrontos():
    global confrontos_atuais
    todos_times = times.listar_times()
    nomes = [t["nome"] for t in todos_times]
    confrontos_atuais = torneios.gerar_confronto(nomes)
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/iniciar", methods=["POST"])
def iniciar_rodada():
    global lista_partidas, tabela_ranking
    resultados = torneios.iniciar_rodada(confrontos_atuais)
    for resultado in resultados:
        lista_partidas.append(resultado)
        tabela_ranking = ranking.atualizar_pontos(tabela_ranking, resultado)
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/avancar", methods=["POST"])
def avancar_fase():
    global confrontos_atuais
    classificados = torneios.avancar_fase(lista_partidas)
    confrontos_atuais = torneios.gerar_confronto(classificados)
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/reiniciar", methods=["POST"])
def reiniciar_torneio():
    global lista_partidas, tabela_ranking, confrontos_atuais
    lista_partidas = []
    tabela_ranking = []
    confrontos_atuais = []
    return redirect(url_for("pagina_torneio"))


@app.route("/ranking")
def pagina_ranking():
    classificacao = ranking.ordenar_classificacao(tabela_ranking)
    return render_template("ranking.html", classificacao=classificacao)


if __name__ == "__main__":
    app.run(debug=True)
