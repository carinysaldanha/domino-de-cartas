# Dominó de Baralho (Terminal Game)

Este é um jogo de **Dominó com Baralho Tradicional**, jogável diretamente no terminal, desenvolvido em Python. O jogo simula uma partida contra 3 bots, respeitando as regras do dominó adaptadas para cartas.

---

## 📌 Regras do Jogo

- Cada jogador recebe 13 cartas (total 52 cartas, baralho padrão sem curingas).
- O jogo começa com os **7 de cada naipe** no centro da mesa.
- É possível jogar apenas a carta imediatamente superior ou inferior à sequência de um determinado naipe.
- Se não houver jogada válida, o jogador pode **passar a vez (digite 0)**.
- Ganha quem primeiro esvaziar a mão.
- Se nenhum jogador puder mais jogar, vence quem tiver a menor quantidade de cartas.

---

## 💻 Como executar

### Pré-requisitos

- Python 3.10 ou superior instalado

### Executando o jogo

1. Clone ou baixe este repositório.
2. No terminal, navegue até o diretório raiz do projeto.
3. Execute o seguinte comando:

```bash
python3 iniciar_jogo.py
