#import "resources/report.typ" as report

#show: report.styling.with(
    hasFooter: false
)

= Avaliação por pares
A104365 Fábio Magalhães DELTA = 0.5 \
A104267 André Pinto DELTA = 0 \
A104540 Pedro Gomes DELTA = 0.5 \
A104185 Filipe Fernandes DELTA = 0 \
A104615 David Costa DELTA = -1

#report.index()

= Introdução
#v(15pt)
Neste relatório exploramos a aplicação de algoritmos de procura no contexto de resolução de problemas, neste caso na distribuição de alimentos e assistência em zonas afetadas por catástrofes naturais. O trabalho visa otimizar a distribuição de alimentos, água e medicamentos de forma eficiente e rápida, priorizando áreas mais necessitadas e limitando o desperdício de recursos enquanto maximizando o número de pessoas assistidas dentro de um tempo limitado.x
A solução proposta deve considerar as restrições operacionais, como a capacidade dos veículos, as condições meteorológicas e de acesso, para maximizar a assistência e salvar vidas.

A utilização de estratégias de procura informada e não informada possibilitará a criação de rotas otimizadas, adaptáveis a cenários dinâmicos e com condições imprevisíveis.

Este estudo foca-se, portanto, na formulação e implementação de algoritmos que possam responder a tais desafios, garantindo uma resposta eficaz em contextos de emergência.



= Descrição do problema
#v(15pt)
Durante uma catástrofe natural, as necessidades de fornecimento de alimentos essenciais e assistência tornam-se críticas para o salvamento de vidas nas zonas mais afetadas.

A tarefa é agravada pela diversidade geográfica e pelas condições meteorológicas que dificultam o acesso a algumas zonas.
Nessas situações, é essencial um sistema de distribuição eficiente que atenda as áreas prioritárias, considerando a gravidade da situação e a densidade populacional de cada local.

Os veículos disponíveis (drones, helicópteros, barcos, camiões, etc.) possuem limitações específicas, como a capacidade de carga e autonomia, que podem ser impactadas por fatores ambientais.
Para maximizar a efetividade da distribuição, é necessário escolher o veículo adequado para cada rota e garantir que os suprimentos cheguem dentro do tempo crítico, isto é, a escolha ótima da rota a tomar considerando o consumo de combustível.

O objetivo central é garantir que o maior número de pessoas seja assistido dentro de um tempo limitado, evitando desperdícios de tempo, alimentos e combustível. Enfrentando obstáculos fixos e dinâmicos, como acessos bloqueados e condições climáticas extremas.


= Formulação do problema
#v(15pt)
- *Estado Inicial:* Alimentos e medicamentos disponíveis e veículos prontos para distribuição.
- *Objetivo:* Maximizar a assistência às áreas prioritárias dentro do tempo limitado.
- *Ações:* Escolha de veículo e rota.
- *Custo:* Baseado no consumo de combustível e tempo de cada rota.


Essa formulação permite aplicar e avaliar algoritmos de procura, comparando a eficiência das soluções.

#pagebreak()


= Metodologia
#v(15pt)
== Modelagem dos Grafos

O sistema utiliza dois tipos principais de grafos:

*FixedGraph:* Representa cenários estáticos, onde as condições das rotas e zonas são fixas.

*DynamicGraph:* Modela cenários dinâmicos, com condições que mudam em tempo real, incluindo acessibilidade, condições climáticas e severidade das zonas.

== Algoritmos Implementados
#v(15pt)
Os seguintes algoritmos foram adaptados para lidar com restrições dinâmicas:

*DFS (Busca em Profundidade):* Explora as rotas até encontrar uma solução ou não haver mais opções.

*BFS (Busca em Largura):* Garante a exploração de todas as rotas em ordem de custo crescente.

*A\* (Busca Informada):* Utiliza heurísticas baseadas na gravidade e densidade populacional.

*Greedy:* Seleciona o próximo passo com base no menor custo heurístico.

*Uniform Cost Search:* Minimiza custos totais considerando combustível e tempo.

*Hill Climbing:* Baseado em heurísticas locais para encontrar soluções rapidamente.

=== Regras e Restrições
#v(15pt)
*Heurísticas:* Calculadas com base na severidade e população das zonas.

*Restrições de Veículos:* Veículos têm limites de capacidade e autonomia.

*Condições Dinâmicas:* Rotas podem mudar devido às condições climáticas.

== Ferramentas Utilizadas
#v(15pt)
*Linguagem:* Python

*Bibliotecas Externas Usadas no Projeto:*

- *colorama* (para colorir mensagens no terminal)

- *geopandas* (para manipulação de dados geoespaciais)

- *networkx* (para análise de grafos e conectividade)

- *osmnx* (para obtenção de mapas e dados de redes rodoviárias)

#v(15pt)

*Módulos Internas do Projeto:*

- *example_graph* (para modelos de grafos fixos e dinâmicos)

- *classes.graph* (para estrutura de grafos)

- *classes.zone* (para definição de zonas)

- *classes.vehicle* (para definição e manipulação de veículos)

- *classes.algorithms* (para algoritmos de busca como BFS, DFS, etc.)

- *utils.notify* (para notificações no terminal)

- *utils.menu* (para criação de menus interativos)


#pagebreak()


= Conclusão e Resultados
#v(15pt)
A escolha do veículo a ser utilizado depende diretamente da carga total que será transportada, considerando as capacidades e restrições operacionais de cada tipo de veículo. Veículos menores, como drones, são ideais para cargas leves e rápidas entregas em zonas de difícil acesso, enquanto camiões ou barcos são mais adequados para transportar grandes quantidades de suprimentos em distâncias maiores. Essa decisão é crucial para garantir que a carga seja distribuída de forma eficiente, minimizando custos e tempo, ao mesmo tempo em que atende às necessidades das zonas afetadas dentro das limitações impostas pelas condições climáticas e geográficas.

As soluções e o custo de cada problema variam significativamente dependendo do tipo de grafo escolhido, seja ele fixo (FixedGraph) ou dinâmico (DynamicGraph). No caso de um grafo fixo, as rotas e as condições entre as zonas permanecem constantes ao longo da execução, permitindo que os algoritmos se concentrem exclusivamente na otimização das rotas com base nos dados iniciais. No entanto, num grafo dinâmico, as condições podem mudar em tempo real, como bloqueios nas rotas ou alterações nas condições climáticas, o que exige que os algoritmos se adaptem constantemente a novas informações. Essas mudanças impactam diretamente tanto o custo das soluções (em termos de combustível e tempo) quanto a eficácia da distribuição, já que as rotas podem ser interrompidas ou alteradas durante o processo. Portanto, a escolha do grafo influencia diretamente a complexidade do problema, a qualidade da solução e os recursos necessários para garantir uma resposta eficaz às necessidades.

Ao executar o código do nosso projeto, o seguinte menu é exibido:
#image("images/menu.png")
Ao selecionarmos, por exemplo, o Fixed Graph, é apresentado o menu:
#pagebreak()

#image("images/menufixedgraph.png") 
Se pedirmos para desenhar o grafo, com a opção 4, obtemos:
#image("images/grafodesenhado.png")

#pagebreak()

Vejamos agora os resultados obtidos para uma carga total de 700 kg a ser transportada, analisando o desempenho de cada algoritmo e considerando um cenário modelado como o FixedGraph representado acima.

*DFS:*
#image("images/DFS.png")
Resultado:['Angola', 'Namibia', 'Botswana', 'Zimbabwe', 'Malawi']

Custo total = 32

Veículo: Camião
#v(15pt)

*BFS:*
#image("images/BFS.png")

Resultado: ['Angola', 'Namibia', 'Zambia', 'Tanzania'] 

Custo total = 11 

Veículo: Helicóptero

*A\*:*
#image("images/a.png")

Resultado: ['Angola', 'Namibia', 'Zambia', 'Tanzania'] 

Custo total = 20 

Veículo: Camião
#v(15pt)

*Greedy:*
#image("images/greedy.png")
Resultado: ['Angola', 'Namibia', 'Botswana', 'Zimbabwe', 'Malawi'] 

Custo total = 32 

Veículo: Camião

#pagebreak()

*Custo Uniforme:*
#image("images/CustoUniforme.png")

Resultado: ['Angola', 'Namibia', 'Botswana', 'Zimbabwe', 'Malawi'] 

Custo total = 59 

Veículo: Camião

#v(15pt)

*Hill Climbing:*
#image("images/HillClimb.png")
Resultado: ['Angola', 'Namibia', 'Botswana', 'Zimbabwe', 'Zambia', 'Tanzania'] 

Custo total = 30 

Veículo: Camião

#v(15pt)
== Observação dos resultados
Sendo assim, os resultados obtidos para a distribuição da carga total igual a 700 kg no fixedGraph exemplificado mostram diferentes desempenhos conforme o algoritmo utilizado:

Ambos os algoritmos *BFS* e *A\** resultaram na mesma solução, com um custo total de 20.
Já os algoritmos *Greedy* e *DFS* passaram por mais locais e tiveram um custo total de 32, visto que foram mais extensivos na procura por soluções.
O algoritmo do Custo Uniforme apresentou o maior custo total, 59.
O *Hill Climbing* obteve uma solução intermediária, com um custo total de 30, explorando mais locais do que o BFS.
Todos os algoritmos utilizaram o camião como veículo, devido a ser o ideal para a carga total de 700kg.
Com base nos resultados apresentados, o *BFS* e o *A\** foram os algoritmos com o menor custo total (20), ambos utilizando o camião como veículo e abrangendo as mesmas localizações.
No entanto, o algoritmo A\* oferece uma solução mais otimizada dependendo da heurística usada (se não fosse pelo custo total idêntico, o *A\** seria o preferido devido à sua capacidade de considerar informações adicionais para otimizar a rota).

Em suma, a implementação de algoritmos de procura no contexto de logística de emergência, combinada com o uso de grafos fixos e dinâmicos, permitiu explorar diferentes estratégias de otimização, levando à escolha de soluções adequadas a contextos específicos. O projeto ressalta a importância de ajustar as abordagens conforme as necessidades do cenário e das restrições operacionais, garantindo uma resposta eficiente e adaptável em situações de emergência.


#pagebreak()


= Referências
#v(15pt)
Russell and Norvig (2009). Artificial Intelligence - A Modern Approach, 3rd edition, ISBN-13: 9780136042594;
\
Costa E., Simões A., (2008), Inteligência Artificial-Fundamentos e Aplicações, FCA, ISBN: 978-972-722-34;
\
Inteligência Artificial, Equipa Docente., (2024), Classical Search, Powerpoint: Blackboard E-learning;
\
Inteligência Artificial, Equipa Docente., (2024), Procura em contextos competitivos, Powerpoint: Blackboard E-learning;
\
Inteligência Artificial, Equipa Docente., (2024), Para além da Procura Clássica, Powerpoint: Blackboard E-learning;