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

    confrontos_pendentes = []
    for c in confrontos_atuais:
        tem_resultado = any(
            (p.get("time1") == c[0] and p.get("time2") == c[1]) or
            (p.get("time1") == c[1] and p.get("time2") == c[0])
            for p in lista_partidas if p.get("rodada") == numero_rodada
        )
        if not tem_resultado:
            confrontos_pendentes.append(c)

    partidas_rodada_atual = [p for p in lista_partidas if p.get("rodada") == numero_rodada]

    return render_template(
        "partidas.html",
        partidas=partidas_filtradas,
        todos_times=todos_times,
        rodadas=rodadas,
        filtro_time=filtro_time,
        filtro_rodada=filtro_rodada,
        msg=msg,
        tipo=tipo,
        confrontos_atuais=confrontos_atuais,
        confrontos_pendentes=confrontos_pendentes,
        partidas_rodada_atual=partidas_rodada_atual,
        numero_rodada=numero_rodada,
    )


@app.route("/partidas/registrar", methods=["POST"])
def registrar_partida():
    global resultados_rodada_atual
    time1 = request.form.get("time1", "").strip()
    time2 = request.form.get("time2", "").strip()

    if not time1 or not time2:
        return redirect(url_for("pagina_partidas", msg="Erro: nomes dos times não podem ser vazios.", tipo="erro"))
    if time1 == time2:
        return redirect(url_for("pagina_partidas", msg="Erro: um time não pode disputar contra si mesmo.", tipo="erro"))

    try:
        gols1 = int(request.form.get("gols_time1", 0))
        gols2 = int(request.form.get("gols_time2", 0))
    except ValueError:
        return redirect(url_for("pagina_partidas", msg="Erro: gols devem ser números inteiros.", tipo="erro"))

    rodada_partida = None
    for c in confrontos_atuais:
        if (c[0] == time1 and c[1] == time2) or (c[1] == time1 and c[0] == time2):
            ja_registrada = any(
                (p.get("time1") == c[0] and p.get("time2") == c[1]) or
                (p.get("time1") == c[1] and p.get("time2") == c[0])
                for p in lista_partidas if p.get("rodada") == numero_rodada
            )
            if ja_registrada:
                return redirect(url_for("pagina_partidas",
                    msg=f"Partida {time1} × {time2} já foi registrada nesta rodada.", tipo="erro"))
            rodada_partida = numero_rodada
            break

    resultado = {"time1": time1, "time2": time2, "gols_time1": gols1, "gols_time2": gols2}
    if rodada_partida:
        resultado["rodada"] = rodada_partida

    lista_partidas.append(resultado)
    ranking.atualizar_pontos(resultado)
    resultados_rodada_atual = [p for p in lista_partidas if p.get("rodada") == numero_rodada]

    return redirect(url_for("pagina_partidas", msg="Partida registrada com sucesso.", tipo="sucesso"))


@app.route("/torneio")
def pagina_torneio():
    todos_times = times.listar_times()
    msg = request.args.get("msg", "")
    tipo = request.args.get("tipo", "")
    rodada_completa = len(confrontos_atuais) > 0 and len(resultados_rodada_atual) >= len(confrontos_atuais)
    return render_template(
        "torneio.html",
        times=todos_times,
        confrontos=confrontos_atuais,
        resultados=resultados_rodada_atual,
        campeao=campeao,
        msg=msg,
        tipo=tipo,
        numero_rodada=numero_rodada,
        rodada_completa=rodada_completa,
    )


@app.route("/torneio/gerar", methods=["POST"])
def gerar_confrontos():
    global confrontos_atuais, resultados_rodada_atual, campeao, numero_rodada, lista_partidas
    nomes = request.form.getlist("times_selecionados")
    if len(nomes) < 2:
        return redirect(url_for("pagina_torneio", msg="Selecione pelo menos 2 times para gerar confrontos.", tipo="erro"))
    if len(nomes) % 2 != 0:
        return redirect(url_for("pagina_torneio", msg="Selecione um número par de times para gerar confrontos.", tipo="erro"))
    ranking.criar_tabela(nomes)
    confrontos_atuais = torneios.gerar_confronto(nomes)
    resultados_rodada_atual = []
    campeao = None
    lista_partidas = []
    numero_rodada = 1
    return redirect(url_for("pagina_torneio"))


@app.route("/torneio/avancar", methods=["POST"])
def avancar_fase():
    global confrontos_atuais, resultados_rodada_atual, campeao, numero_rodada
    if len(resultados_rodada_atual) < len(confrontos_atuais):
        return redirect(url_for("pagina_torneio",
            msg="Registre os resultados de todas as partidas na página de Partidas antes de avançar.", tipo="erro"))
    classificados = torneios.avancar_fase(resultados_rodada_atual)
    if len(classificados) == 1:
        campeao = classificados[0]
        confrontos_atuais = []
        resultados_rodada_atual = []
    else:
        numero_rodada += 1
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
