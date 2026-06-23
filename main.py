import os
import threading
from flask import Flask, render_template, request, redirect, url_for
import times, partidas, torneios, ranking

times.inicializar()
partidas.inicializar()
ranking.inicializar()
torneios.inicializar()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/times")
def pagina_times():
    todos_times = times.listar_times()["dados"]
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    busca_id = request.args.get("busca_id", "").strip()
    resultado_busca = None
    if busca_id:
        res = times.buscar_time(busca_id)
        resultado_busca = res["dados"] if res["status"] == 0 else None
    return render_template("times.html", times=todos_times, msg=msg, tipo=tipo,
                           busca_id=busca_id, resultado_busca=resultado_busca)


@app.route("/times/criar", methods=["POST"])
def criar_time():
    nome = request.form.get("nome", "").strip()
    jogadores_raw = request.form.get("jogadores", "").strip()
    jogadores = times.parsear_jogadores(jogadores_raw)["dados"]
    resultado = times.criar_time(nome, jogadores)
    if resultado["status"] == 0:
        return redirect(url_for("pagina_times", msg=f"Time '{resultado['dados']['nome']}' criado com sucesso.", tipo="sucesso"))
    return redirect(url_for("pagina_times", msg=resultado["mensagem"], tipo="erro"))


@app.route("/times/remover/<identificador>")
def remover_time(identificador):
    resultado = times.remover_time(identificador)
    if resultado["status"] == 1:
        return redirect(url_for("pagina_times", msg=resultado["mensagem"], tipo="erro"))
    return redirect(url_for("pagina_times", msg=f"Time '{resultado['dados']['nome']}' removido com sucesso.", tipo="sucesso"))


@app.route("/partidas")
def pagina_partidas():
    todos_times = times.listar_times()["dados"]
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    filtro_time = request.args.get("filtro_time", "").strip()
    filtro_rodada = request.args.get("filtro_rodada", "").strip()
    filtro_torneio = request.args.get("filtro_torneio", "").strip()

    torneio_ativo = torneios.get_ativo()["dados"]
    torneio_ativo_id = torneio_ativo["id"] if torneio_ativo else None
    numero_rodada = torneio_ativo["rodada"] if torneio_ativo else 0

    torneio_id_historico = filtro_torneio or None
    pendentes = torneios.confrontos_pendentes()["dados"] or []

    return render_template(
        "partidas.html",
        partidas=partidas.listar(filtro_time or None, filtro_rodada or None, torneio_id=torneio_id_historico)["dados"],
        todos_times=todos_times,
        todos_torneios=torneios.listar()["dados"],
        rodadas=partidas.rodadas(torneio_id=torneio_id_historico)["dados"],
        filtro_time=filtro_time,
        filtro_rodada=filtro_rodada,
        filtro_torneio=filtro_torneio,
        msg=msg,
        tipo=tipo,
        confrontos_atuais=torneio_ativo["confrontos"] if torneio_ativo else [],
        confrontos_pendentes=pendentes,
        partidas_rodada_atual=partidas.por_rodada(numero_rodada, torneio_id=torneio_ativo_id)["dados"],
        numero_rodada=numero_rodada,
    )


@app.route("/partidas/registrar", methods=["POST"])
def registrar_partida():
    time1 = request.form.get("time1", "").strip()
    time2 = request.form.get("time2", "").strip()

    try:
        gols1 = int(request.form.get("gols_time1", 0))
        gols2 = int(request.form.get("gols_time2", 0))
    except ValueError:
        return redirect(url_for("pagina_partidas", msg="Erro: gols devem ser números inteiros.", tipo="erro"))

    ctx = torneios.contexto_partida(time1, time2)
    if ctx["status"] == 1:
        return redirect(url_for("pagina_partidas",
            msg="Registre apenas confrontos da rodada atual do torneio ativo.", tipo="erro"))
    torneio_id, rodada = ctx["dados"]

    resultado = partidas.registrar(time1, time2, gols1, gols2, rodada, torneio_id)
    if resultado["status"] == 1:
        return redirect(url_for("pagina_partidas", msg=resultado["mensagem"], tipo="erro"))

    ranking.atualizar_pontos(resultado["dados"], torneio_id=torneio_id or "default")
    return redirect(url_for("pagina_partidas", msg="Partida registrada com sucesso.", tipo="sucesso"))


@app.route("/torneio")
def pagina_torneio():
    todos_times = times.listar_times()["dados"]
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    torneio_ativo = torneios.get_ativo()["dados"]
    numero_rodada = torneio_ativo["rodada"] if torneio_ativo else 0
    pendentes = torneios.confrontos_pendentes()["dados"] or []
    return render_template(
        "torneio.html",
        times=todos_times,
        torneio_ativo=torneio_ativo,
        todos_torneios=torneios.listar()["dados"],
        confrontos=torneio_ativo["confrontos"] if torneio_ativo else [],
        resultados=partidas.por_rodada(
            numero_rodada,
            torneio_id=torneio_ativo["id"] if torneio_ativo else None
        )["dados"],
        campeao=torneio_ativo["campeao"] if torneio_ativo else None,
        msg=msg,
        tipo=tipo,
        numero_rodada=numero_rodada,
        rodada_completa=not pendentes,
    )


@app.route("/torneio/gerar", methods=["POST"])
def gerar_confrontos():
    nomes = request.form.getlist("times_selecionados")
    nome_torneio = request.form.get("nome_torneio", "").strip()
    torneio = torneios.criar(nome_torneio, nomes)
    if torneio["status"] == 1:
        return redirect(url_for("pagina_torneio", msg=torneio["mensagem"], tipo="erro"))
    ranking.criar_tabela(nomes, torneio_id=torneio["dados"]["id"])
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/ativar/<torneio_id>", methods=["POST"])
def ativar_torneio(torneio_id):
    r = torneios.set_ativo(torneio_id)
    return redirect(url_for("pagina_torneio", msg=r["mensagem"], tipo="sucesso" if r["status"] == 0 else "erro"))


@app.route("/torneio/avancar", methods=["POST"])
def avancar_fase():
    pendentes = torneios.confrontos_pendentes()["dados"]
    if pendentes:
        return redirect(url_for("pagina_torneio",
            msg="Registre os resultados de todas as partidas na página de Partidas antes de avançar.", tipo="erro"))
    r = torneios.avancar()
    return redirect(url_for("pagina_torneio", msg=r["mensagem"], tipo="sucesso" if r["status"] == 0 else "erro"))


@app.route("/torneio/reiniciar", methods=["POST"])
def reiniciar_torneio():
    torneio_ativo = torneios.get_ativo()["dados"]
    if torneio_ativo:
        partidas.resetar(torneio_id=torneio_ativo["id"])
        ranking.criar_tabela(torneio_ativo["times"], torneio_id=torneio_ativo["id"])
    torneios.resetar_ativo()
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/encerrar", methods=["POST"])
def encerrar_torneio():
    torneios.desativar()
    return redirect(url_for("pagina_torneio"))


@app.route("/ranking")
def pagina_ranking():
    torneio_id = request.args.get("torneio_id", "").strip()
    todos_torneios = torneios.listar()["dados"]
    if torneio_id:
        res = ranking.ordenar_classificacao(torneio_id)
        classificacao = res["dados"] if res["status"] == 0 else []
    else:
        classificacao = []
    torneio_selecionado = next((t for t in todos_torneios if t["id"] == torneio_id), None)
    return render_template(
        "ranking.html",
        classificacao=classificacao,
        todos_torneios=todos_torneios,
        torneio_id=torneio_id,
        torneio_selecionado=torneio_selecionado,
    )


@app.route("/encerrar", methods=["POST"])
def encerrar():
    times.salvar()
    partidas.salvar()
    torneios.salvar()
    ranking.salvar()
    threading.Timer(1.0, lambda: os._exit(0)).start()
    return render_template("encerrar.html")


if __name__ == "__main__":
    app.run(debug=True)
