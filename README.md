# 🏆 Simulador de Torneios

> Trabalho da disciplina **Programação Modular** — Turma 3WA  
> Professor: Flávio Heleno Bevilacqua e Silva

## 👥 Integrantes

| Matrícula | Nome |
|-----------|------|
| 2421312 | Julia Kymie Dias Okada |
| 2320715 | Lucas Manoel Martins de Souza |
| 2320450 | Maria Eduarda Fonte de Macedo |
| 2511621 | Pedro Henrique Vargas Mucelin |

## 📋 Descrição do Projeto

Sistema de criação e gerenciamento de torneios esportivos. A partir de uma lista de times cadastrados, o sistema gera confrontos aleatórios, simula partidas, registra resultados e mantém um ranking atualizado. Ao final de cada rodada, o sistema avança para a próxima fase com base nos resultados.

## ⚙️ Requisitos e Restrições

- **Linguagem:** Python puro
- **Proibido:** criação de classes/objetos pelos alunos
- Bibliotecas de terceiros (ex.: frameworks de teste) são permitidas, desde que não exijam a programação de novas classes
- Nenhuma outra linguagem além de Python é aceita

## 🗂️ Estrutura de Módulos

```
simulador_torneios/
│
├── times.py              # Módulo de gerenciamento de times
├── partidas.py           # Módulo de simulação e registro de partidas
├── torneios.py           # Módulo de gerenciamento de rodadas e fases
├── ranking.py            # Módulo de classificação
│
├── test_times.py         # Testador do módulo Times
├── test_partidas.py      # Testador do módulo Partidas
├── test_torneios.py      # Testador do módulo Torneios
├── test_ranking.py       # Testador do módulo Ranking
│
└── main.py               # Programa principal (interface web / ponto de entrada)
```

## 📦 Módulos

### `times.py` — Gerenciamento de Times
**Responsável:** Julia Kymie Dias Okada  
**Testador:** `test_times.py`

Gerencia o ciclo de vida dos times: criação, consulta, listagem e remoção.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `criar_time` | `(nome: str, jogadores: list[str]) → dict` | Cria um time com ID único gerado automaticamente |
| `buscar_time` | `(identificador: str) → dict \| None` | Retorna os dados de um time pelo ID |
| `listar_times` | `() → list[dict]` | Retorna todos os times cadastrados |
| `remover_time` | `(identificador: str) → bool` | Remove um time pelo ID |

---

### `partidas.py` — Simulação e Registro de Partidas
**Responsável:** Lucas Manoel Martins de Souza  
**Testador:** `test_partidas.py`

Simula partidas entre times e registra os resultados.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `simular_partida` | `(time1: str, time2: str) → dict` | Gera resultado aleatório de uma partida |
| `gerar_resultado` | `(partida: dict) → str` | Formata o resultado de uma partida como string |
| `registrar_resultado` | `(lista_partidas: list, time1: str, time2: str, gols_time1: int, gols_time2: int) → dict` | Insere o resultado em uma lista de partidas |
| `listar_partidas` | `(lista_partidas: list) → list` | Lista todas as partidas registradas |

---

### `torneios.py` — Gerenciamento de Rodadas e Fases
**Responsável:** Pedro Henrique Vargas Mucelin  
**Testador:** `test_torneios.py`

Controla o fluxo competitivo: geração de confrontos, rodadas e avanço de fases.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `gerar_confronto` | `(lista_times: list[str]) → list[tuple]` | Gera pares de confronto aleatórios |
| `iniciar_rodada` | `(confrontos: list[tuple]) → list[dict]` | Simula todas as partidas de uma rodada |
| `avancar_fase` | `(resultados: list[dict]) → list[str]` | Seleciona os times classificados para a próxima fase |

---

### `ranking.py` — Classificação
**Responsável:** Maria Eduarda Fonte de Macedo  
**Testador:** `test_ranking.py`

Cria e mantém a tabela de classificação atualizada.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `criar_tabela` | `(lista_times: list[str]) → list[dict]` | Inicializa tabela com todos os contadores zerados |
| `atualizar_pontos` | `(tabela: list[dict], resultado: dict) → list[dict]` | Atualiza pontos após cada partida (vitória=3pts, empate=1pt) e retorna a tabela atualizada |
| `ordenar_classificacao` | `(tabela: list[dict]) → list[dict]` | Ordena por pontos → vitórias → saldo de gols (sem modificar o original) |
| `mostrar_classificacao` | `(tabela: list[dict]) → str` | Exibe a tabela formatada no terminal e retorna a tabela como string formatada |

---

## 🌿 Branches

Cada responsável trabalha na sua própria branch e passar para `main` quando o módulo estiver pronto.

| Branch | Responsável | Conteúdo |
|--------|-------------|----------|
| `main` | — | Código estável e integrado |
| `modulo/times` | Julia Kymie Dias Okada | `times.py` + `test_times.py` |
| `modulo/partidas` | Lucas Manoel Martins de Souza | `partidas.py` + `test_partidas.py` |
| `modulo/torneios` | Pedro Henrique Vargas Mucelin | `torneios.py` + `test_torneios.py` |
| `modulo/ranking` | Maria Eduarda Fonte de Macedo | `ranking.py` + `test_ranking.py` |
| `front` | Julia Kymie Dias Okada e Lucas Manoel Martins de Souza | `main.py` + `templates/` |

### Fluxo de trabalho

```bash
# Criar e entrar na sua branch (exemplo para times)
git checkout -b modulo/times

# Trabalhar normalmente, commitar e subir
git add times.py test_times.py
git commit -m "feat: implementa módulo times"
git push origin modulo/times
```

---

## ✅ Executando os Testes

Cada módulo (exceto o principal) possui seu próprio módulo testador. Para executar todos os testes:

```bash
# Testes individuais por módulo
python test_times.py
python test_partidas.py
python test_torneios.py
python test_ranking.py
```

Os módulos testadores devem ser executados sem erros e apresentar um relatório cobrindo todos os casos de teste previstos.

> **Requisito:** cada função de acesso de cada módulo deve ter casos de teste que exercitem **todos os retornos previstos** pela sua interface.

## 🧪 Casos de Teste

### Módulo `times.py`

**`criar_time`**
- ✅ Time criado com sucesso → retorna `dict` com `id`, `nome` e `jogadores`
- ✅ Time sem jogadores → retorna `dict` com `jogadores: []`

**`buscar_time`**
- ✅ Time encontrado → retorna `dict` com os dados do time
- ✅ ID inexistente → `"Erro: time com ID 'zzzzzz' não encontrado."`
- ✅ ID vazio → `"Erro: ID não pode ser vazio."`

**`listar_times`**
- ✅ Com times cadastrados → retorna lista de dicionários
- ✅ Sem times cadastrados → retorna `[]`

**`remover_time`**
- ✅ Remoção bem-sucedida → `"Time 'Flamengo' removido com sucesso."`
- ✅ ID inexistente → `"Erro: time com ID 'zzzzzz' não encontrado."`
- ✅ ID vazio → `"Erro: ID não pode ser vazio."`

---

### Módulo `torneios.py`

**`gerar_confronto`**
- ✅ Lista com número par de times → N/2 pares
- ✅ Lista com 2 times → 1 par
- ✅ Lista vazia → retorna `[]` sem erros

**`iniciar_rodada`**
- ✅ Múltiplos confrontos → lista com resultados de cada partida
- ✅ Confronto único → lista com 1 resultado
- ✅ Lista vazia → retorna `[]` sem erros

**`avancar_fase`**
- ✅ Vencedor claro → time com mais gols avança
- ✅ Empate → ambos avançam (ou critério de desempate)
- ✅ Múltiplas partidas → cada vencedor avança

---

### Módulo `ranking.py`

**`criar_tabela`**
- ✅ Múltiplos times → tabela com todos os contadores zerados
- ✅ Nome preservado corretamente
- ✅ Lista vazia → retorna `[]` sem erros

**`atualizar_pontos`**
- ✅ Vitória do time1 → retorna tabela com time1: pontos=3, vitórias=1 / time2: pontos=0, derrotas=1
- ✅ Vitória do time2 → retorna tabela com time2: pontos=3, vitórias=1 / time1: pontos=0, derrotas=1
- ✅ Empate → retorna tabela com ambos: pontos=1, empates=1
- ✅ Gols contabilizados → retorna tabela com `gols_marcados` e `gols_sofridos` atualizados
- ✅ Acumulativo após múltiplas partidas → retorna tabela com totais somados corretamente

**`ordenar_classificacao`**
- ✅ Ordenação por pontos
- ✅ Desempate por vitórias
- ✅ Desempate por saldo de gols
- ✅ Tabela original não é modificada

**`mostrar_classificacao`**
- ✅ Retorna a tabela formatada como string (não `None`)
- ✅ Tabela não é modificada após exibição
- ✅ Tabela vazia → retorna string vazia ou mensagem, sem erros

---

### Módulo `partidas.py`

**`simular_partida`**
- ✅ Mesmo time duas vezes → `{"erro": "Um time não pode disputar contra si mesmo"}`
- ✅ Nome de time vazio → `{"erro": "Nome dos times não pode ser vazio"}`
- ✅ Chamada correta → `{"time1": ..., "time2": ..., "gols_time1": N, "gols_time2": N}`

**`gerar_resultado`**
- ✅ Partida com erro → retorna a mensagem de erro
- ✅ Partida válida → ex.: `"Vasco 3 x Botafogo 5"`

**`registrar_resultado`**
- ✅ Mesmo time duas vezes → `{"erro": "Um time não pode disputar contra si mesmo"}`
- ✅ Nome de time vazio → `{"erro": "Nome dos times não pode ser vazio"}`
- ✅ Chamada correta → insere e retorna o dicionário da partida

**`listar_partidas`**
- ✅ Lista com partidas → retorna lista de dicionários
- ✅ Lista vazia → `"Lista vazia"`

## 🔗 Testes de Integração

Os testes integrados encadeiam funções de todos os módulos, garantindo que a comunicação entre eles ocorre corretamente.

**Fluxo 1 — Rodada única:** criação de 4 times → tabela → confrontos → rodada → registro dos resultados → atualização dos pontos → exibição da classificação.

**Fluxo 2 — Torneio com avanço de fases:** 2 rodadas completas com classificados avançando entre fases, acumulando pontuação.

**Fluxo 3 — Validação de erros:** nome inválido ao criar time e time disputando contra si mesmo não interrompem o sistema; erros são retornados de forma descritiva e os dados válidos são preservados.

## 📐 Requisitos Não Funcionais

- Sistema modular com responsabilidades separadas por domínio
- Funções testáveis isoladamente
- Validação de entradas inválidas com mensagens de erro descritivas (sem interromper a execução)
- Sem efeitos colaterais inesperados sobre estruturas de dados compartilhadas
- Nomenclatura padronizada em português

## 🌐 Interface Web

O sistema também pode ser acessado via interface web, onde é possível incluir, excluir, editar e gerenciar torneios e partidas.

**Front-end:** Julia Kymie Dias Okada e Lucas Manoel Martins de Souza
