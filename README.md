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

Sistema de criação e gerenciamento de torneios esportivos. A partir de uma lista de times cadastrados, o usuário seleciona quais participam do torneio, o sistema gera confrontos aleatórios, registra resultados manualmente ou de forma randomizada, mantém um ranking atualizado e avança as fases automaticamente até definir o campeão.

## ⚙️ Requisitos e Restrições

- **Linguagem:** Python puro
- **Proibido:** criação de classes/objetos pelos alunos
- Bibliotecas de terceiros (ex.: frameworks de teste) são permitidas, desde que não exijam a programação de novas classes
- Nenhuma outra linguagem além de Python é aceita

## 🗂️ Estrutura de Arquivos

```
simulador_torneios/
│
├── times.py              # Gerenciamento de times
├── partidas.py           # Registro e consulta de partidas
├── torneios.py           # Estado e lógica do torneio
├── ranking.py            # Tabela de classificação
│
├── test_times.py         # Testes do módulo Times
├── test_partidas.py      # Testes do módulo Partidas
├── test_torneios.py      # Testes do módulo Torneios
├── test_ranking.py       # Testes do módulo Ranking
│
├── dados_iniciais.json   # Times pré-cadastrados carregados na inicialização
├── main.py               # Roteamento web (ponto de entrada)
└── templates/            # Páginas HTML
```

## 📦 Módulos

### `times.py` — Gerenciamento de Times
**Responsável:** Julia Kymie Dias Okada  
**Testador:** `test_times.py`

Gerencia o ciclo de vida dos times: criação, consulta, listagem e remoção. Na inicialização, carrega automaticamente os times definidos em `dados_iniciais.json`.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `criar_time` | `(nome: str, jogadores: list[str]) → dict \| str` | Cria um time com ID único; retorna o dict ou mensagem de erro |
| `buscar_time` | `(identificador: str) → dict \| str` | Retorna os dados de um time pelo ID ou mensagem de erro |
| `listar_times` | `() → list[dict]` | Retorna todos os times cadastrados |
| `remover_time` | `(identificador: str) → str` | Remove um time pelo ID; retorna mensagem de sucesso ou erro |

---

### `partidas.py` — Registro e Consulta de Partidas
**Responsável:** Lucas Manoel Martins de Souza  
**Testador:** `test_partidas.py`

Única fonte de verdade para o estado das partidas. Registra, filtra e expõe os resultados para os demais módulos.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `registrar` | `(time1: str, time2: str, gols1: int, gols2: int, rodada=None) → dict \| str` | Valida e registra uma partida; retorna o dict criado ou mensagem de erro |
| `listar` | `(filtro_time=None, filtro_rodada=None) → list[dict]` | Retorna partidas com filtros opcionais por time ou rodada |
| `por_rodada` | `(rodada) → list[dict]` | Retorna todas as partidas de uma rodada específica |
| `rodadas` | `() → list[str]` | Retorna a lista ordenada de rodadas com partidas registradas |
| `resetar` | `() → None` | Limpa todas as partidas (usado ao reiniciar o torneio) |

---

### `torneios.py` — Estado e Lógica do Torneio
**Responsável:** Pedro Henrique Vargas Mucelin  
**Testador:** `test_torneios.py`

Gerencia o estado do torneio em andamento e expõe funções puras para geração de confrontos e avanço de fases.

**Funções de estado:**

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `iniciar` | `(nomes: list[str]) → None` | Inicia o torneio com os times selecionados (rodada 1) |
| `get_confrontos` | `() → list[tuple]` | Retorna os confrontos da rodada atual |
| `get_rodada` | `() → int` | Retorna o número da rodada atual |
| `get_campeao` | `() → str \| None` | Retorna o campeão se o torneio encerrou, senão `None` |
| `confrontos_pendentes` | `() → list[tuple]` | Retorna confrontos ainda sem resultado registrado |
| `rodada_completa` | `() → bool` | `True` se todos os confrontos da rodada têm resultado |
| `avancar` | `() → None` | Avança para a próxima fase ou define o campeão |
| `resetar` | `() → None` | Zera o estado do torneio |

**Funções puras:**

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `gerar_confronto` | `(lista_times: list[str]) → list[tuple]` | Gera pares de confronto aleatórios |
| `iniciar_rodada` | `(confrontos: list[tuple]) → list[dict]` | Simula resultados aleatórios para uma rodada |
| `avancar_fase` | `(resultados: list[dict]) → list[str]` | Retorna os times classificados para a próxima fase |

---

### `ranking.py` — Classificação
**Responsável:** Maria Eduarda Fonte de Macedo  
**Testador:** `test_ranking.py`

Cria e mantém a tabela de classificação atualizada com pontos, vitórias, saldo de gols e demais estatísticas.

| Função | Assinatura | Descrição |
|--------|-----------|-----------|
| `criar_tabela` | `(lista_times: list[str]) → int` | Inicializa tabela com todos os contadores zerados |
| `atualizar_pontos` | `(resultado: dict) → int` | Atualiza pontos após cada partida (vitória=3pts, empate=1pt) |
| `ordenar_classificacao` | `() → list[dict]` | Ordena por pontos → vitórias → saldo de gols (sem modificar o original) |
| `mostrar_classificacao` | `() → int` | Exibe a tabela formatada no terminal |


---

## ✅ Executando os Testes

```bash
python test_times.py
python test_partidas.py
python test_torneios.py
python test_ranking.py
```

> **Requisito:** cada função de acesso de cada módulo deve ter casos de teste que exercitem **todos os retornos previstos** pela sua interface.

---

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

### Módulo `partidas.py`

**`registrar`**
- ✅ Chamada correta → retorna `dict` com os dados da partida
- ✅ Nome de time vazio → retorna mensagem de erro
- ✅ Mesmo time duas vezes → retorna mensagem de erro
- ✅ Partida já registrada na mesma rodada → retorna mensagem de erro

**`listar`**
- ✅ Sem filtros → retorna todas as partidas
- ✅ Filtro por time → retorna apenas partidas daquele time
- ✅ Filtro por rodada → retorna apenas partidas daquela rodada
- ✅ Sem partidas → retorna `[]`

**`por_rodada`**
- ✅ Rodada com partidas → retorna lista de dicts
- ✅ Rodada sem partidas → retorna `[]`

**`rodadas`**
- ✅ Com partidas registradas → retorna lista ordenada de rodadas
- ✅ Sem partidas → retorna `[]`

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
- ✅ Empate → ambos avançam
- ✅ Múltiplas partidas → cada vencedor avança

---

### Módulo `ranking.py`

**`criar_tabela`**
- ✅ Múltiplos times → tabela com todos os contadores zerados
- ✅ Nome preservado corretamente
- ✅ Lista vazia → retorna `[]` sem erros

**`atualizar_pontos`**
- ✅ Vitória do time1 → time1: pontos=3, vitórias=1 / time2: pontos=0, derrotas=1
- ✅ Vitória do time2 → time2: pontos=3, vitórias=1 / time1: pontos=0, derrotas=1
- ✅ Empate → ambos: pontos=1, empates=1
- ✅ Gols contabilizados → `gols_marcados` e `gols_sofridos` atualizados
- ✅ Acumulativo após múltiplas partidas → totais somados corretamente

**`ordenar_classificacao`**
- ✅ Ordenação por pontos
- ✅ Desempate por vitórias
- ✅ Desempate por saldo de gols
- ✅ Tabela original não é modificada

**`mostrar_classificacao`**
- ✅ Retorna 0 com sucesso
- ✅ Tabela não é modificada após exibição
- ✅ Tabela vazia → sem erros

---

## 🔗 Testes de Integração

**Fluxo 1 — Rodada única:** criação de 4 times → tabela → confrontos → registro dos resultados → atualização dos pontos → exibição da classificação.

**Fluxo 2 — Torneio com avanço de fases:** 2 rodadas completas com classificados avançando entre fases, acumulando pontuação.

**Fluxo 3 — Validação de erros:** nome inválido ao criar time e time disputando contra si mesmo não interrompem o sistema; erros são retornados de forma descritiva e os dados válidos são preservados.

---

## 📐 Requisitos Não Funcionais

- Sistema modular com responsabilidades separadas por domínio
- Funções testáveis isoladamente
- `main.py` sem lógica de negócio ou estado próprio — apenas roteamento
- Validação de entradas inválidas com mensagens de erro descritivas
- Sem efeitos colaterais inesperados sobre estruturas de dados compartilhadas
- Nomenclatura padronizada em português

---

## 🌐 Interface Web

Acessível via navegador após executar `python main.py`.

**Front-end:** Julia Kymie Dias Okada e Lucas Manoel Martins de Souza

| Página | Funcionalidades |
|--------|----------------|
| **Times** | Cadastrar, buscar e remover times |
| **Torneio** | Selecionar times participantes (número par obrigatório), gerar confrontos, avançar fase, reiniciar |
| **Partidas** | Visualizar confrontos da rodada atual, registrar placar manualmente ou randomizar 🎲, filtrar histórico |
| **Ranking** | Tabela de classificação com pontos, vitórias, empates, derrotas e saldo de gols |

```bash
python main.py
# Acesse http://127.0.0.1:5000
```
