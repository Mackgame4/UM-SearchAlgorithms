#import "resources/report.typ" as report

#show: report.styling.with(
    hasFooter: false
)

#report.index()

= Introdução
#v(15pt)
Neste relatório exploramos a aplicação de algoritmos de procura no contexto de resolução de problemas, neste caso na distribuição de alimentos e assistência em zonas afetadas por catástrofes naturais. O trabalho visa otimizar a distribuição de alimentos, água e medicamentos de forma eficiente e rápida, priorizando áreas mais necessitadas e limitando o desperdício de recursos enquanto maximizando o número de pessoas assistidas dentro de um tempo limitado.
A solução proposta deve considerar as restrições operacionais, como a capacidade dos veículos, as condições meteorológicas e de acesso, para maximizar a assistência e salvar vidas.

A utilização de estratégias de procura informada e não informada possibilitará a criação de rotas otimizadas, adaptáveis a cenários dinâmicos e com condições imprevisíveis.

Este estudo foca-se, portanto, na formulação e implementação de algoritmos que possam responder a tais desafios, garantindo uma resposta eficaz em contextos de emergência.

#pagebreak()

= Descrição do problema
#v(15pt)
Durante uma catástrofe natural, as necessidades de fornecimento de alimentos essenciais e assistência tornam-se críticas para o salvamento de vidas nas zonas mais afetadas.

A tarefa é agravada pela diversidade geográfica e pelas condições meteorológicas que dificultam o acesso a algumas zonas.
Nessas situações, é essencial um sistema de distribuição eficiente que atenda as áreas prioritárias, considerando a gravidade da situação e a densidade populacional de cada local.

Os veículos disponíveis (drones, helicópteros, barcos, caminhões, etc.) possuem limitações específicas, como a capacidade de carga e autonomia, que podem ser impactadas por fatores ambientais.
Para maximizar a efetividade da distribuição, é necessário escolher o veículo adequado para cada rota e garantir que os suprimentos cheguem dentro do tempo crítico, isto é, a escolha ótima da rota a tomar considerando o consumo de combustível.

O objetivo central é garantir que o maior número de pessoas seja assistido dentro de um tempo limitado, evitando desperdícios de tempo, alimentos e combustível. Enfrentando obstáculos fixos e dinâmicos, como acessos bloqueados e condições climáticas extremas.

= Formulação do problema
#v(15pt)
- Estado Inicial: Alimentos e medicamentos disponíveis e veiculos prontos para distribuição.
- Objetivo: Maximizar a assistência às áreas prioritárias dentro do tempo limitado.
- Ações: Escolha de veículo e rota.
- Custo: Baseado no consumo de combustível e tempo de cada rota.

Essa formulação permite aplicar e avaliar algoritmos de procura, comparando a eficiência das soluções.

= Metodologia
#v(15pt)
<\<Descrição de todas as tarefas realizadas, bem como de todas as decisões tomadas pelo grupo de
trabalho>>

#pagebreak()

= Conclusão e Resultados
#v(15pt)
<\<Sumário e discussão dos resultados obtidos>>

#pagebreak()

= Referências
#v(15pt)
<\<Referencias>>