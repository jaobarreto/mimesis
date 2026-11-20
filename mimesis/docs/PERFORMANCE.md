# Protocolo de desempenho local

**Ambiente alvo informado.** Dell Inspiron 15 3520, Intel Core i5-1235U, 16 GB de RAM, SSD de 512 GB e Ubuntu Linux, sem GPU dedicada. Estes valores descrevem o equipamento. Memória disponível, espaço livre, velocidade do SSD e estado térmico variam por execução. Research não inclui medições nem tetos validados.

| Operação | O que medir | Variáveis a manter |
|---|---|---|
| Compilar e atualizar a MKB | Tempo total, CPU de usuário/sistema, RSS máxima, bytes finais e temporários, espaço durante retenção da versão anterior. | Mesmos insumos, ordem, perfil FTS, versões e método de ativação. |
| Primeira consulta | Tempo de abertura, validação e consulta em processo novo. | Distinguir processo frio de cache de disco frio. Anotar se o cache do SO foi controlado. |
| Consultas em regime | p50, p95 e p99 de tempo de parede do pedido completo, também por método, tamanho e classe. | Mesmo lote, ordem alternada, aquecimento declarado, número de repetições e concorrência. |
| Custo de CPU e memória | Tempo de CPU por consulta ou lote e pico de RSS em processos isolados por condição. | Registrar unidade do sistema, número de threads e se filhos foram contabilizados. |
| Crescimento | Índice, tabelas e repertório em bytes, bytes por prompt e diferença de tamanho por registro adicional. | Lotes crescentes com distribuição linguística e comprimentos documentados. |

**Procedimento proposto.** Registrar modelo, RAM/disco livres, SO, kernel, runtime, SQLite/FTS5, versões do corpus e código, perfil de energia e alimentação. Começar com lote curado pequeno. Medir escalas crescentes que caibam em disco com cópia temporária e folga operacional. Preservar as amostras brutas de um relógio monotônico. Repetir as condições e comparar mediana entre execuções. Informar quantidade de observações, dispersão e limitações dos percentis extremos. [Python, consumo de recursos em Unix](https://docs.python.org/3/library/resource.html)

Se o fuzzy exaustivo ultrapassar o orçamento, ensaiar pré-seleção e medir a perda de recall do conjunto candidato contra a busca completa. Se FTS aumentar custo de construção, medir amortização pelo número de consultas. Quando duas estratégias passam pelos limites e uma melhora precisão à custa de latência, publicar os dois eixos e explicitar o custo de erro escolhido para o produto.

**Questão pendente.** Fixar limites numéricos de p95, pico de RSS, espaço temporário e tempo de compilação após piloto em desenvolvimento. Versionar esses limites antes de avaliar o teste reservado. Rodadas com paginação intensa, falta de disco ou interrupção são resultados operacionais e precisam constar no denominador. [Avaliação](EVALUATION.md) · [Seleção da stack](STACK.md)
