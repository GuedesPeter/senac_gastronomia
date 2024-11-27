# POSTMORTEM

## Senac Gastronomia
________________________________________
###  Visão Geral do Projeto

O projeto visava o desenvolvimento de um sistema de gerenciamento de estoque e controle financeiro para o curso de gastronomia da faculdade Senac, com foco na otimização de processos de compra, controle de validade dos produtos e geração de relatórios financeiros. A solução foi projetada para gerenciar produtos alimentícios utilizados nas aulas, monitorando a validade dos insumos e fornecendo uma visão clara e organizada do estoque.
O sistema foi desenvolvido utilizando Python com o framework Django, e a persistência dos dados foi garantida por bancos de dados SQLite 3 e PostgreSQL.
O Que Funcionou Bem
1.	### Execução das Funcionalidades Principais

-	A implementação das funcionalidades de cadastro, edição, exclusão de produtos, e controle de validade foi bem-sucedida. A possibilidade de adicionar, editar e excluir itens no estoque de maneira intuitiva atendeu às necessidades do usuário final de forma eficaz.
-	A funcionalidade de alertas para produtos com validade próxima foi muito útil, ajudando a reduzir desperdícios e garantindo o uso adequado dos alimentos.
-	A filtragem de produtos por diferentes critérios (categoria, fornecedor, etc.) e a geração de relatórios financeiros foram recursos altamente valorizados pelos usuários, proporcionando uma visão detalhada e personalizada do estoque e custos.
2.	### Usabilidade e Interface

-	A interface foi projetada com Bootstrap 5, oferecendo um layout responsivo e fácil de usar.
-	A experiência do usuário foi facilitada pelas mensagens de notificação, como alertas para itens vencidos, o que aumentou a eficiência no gerenciamento do estoque.


________________________________________
## O Que Poderia Ter Sido Feito de Maneira Diferente
1.	### Planejamento e Definição de Requisitos
-	Embora o escopo inicial tenha sido bem delineado, a definição mais precisa de algumas funcionalidades (como relatórios financeiros mais complexos e integrações futuras com outros sistemas acadêmicos) poderia ter sido realizada desde o início para evitar 
2.	### Testes e Validação

-	Testes de carga e performance poderiam ter sido realizados com mais antecedência, dado  grande volume de dados esperado no futuro, o que ajudaria a identificar potenciais gargalos no sistema antes da implantação.
________________________________________
## Aprendizados para Projetos Futuros
1.	### Importância do Planejamento Antecipado
-	Definir com maior clareza as funcionalidades de alto nível e as expectativas dos usuários finais desde o início é essencial para evitar mudanças de escopo e ajustes inesperados. A manutenção da comunicação constante com os stakeholders ajudará a alinhar os requisitos e a evitar surpresas no meio do projeto.
2.	### Gestão de Requisitos e Expectativas
-	Um planejamento mais robusto para prever necessidades futuras, como integrações com outros sistemas e recursos adicionais, pode evitar a reabertura de escopo no meio do projeto.
3.	### Iteração e Testes Continuados
-	Realizar mais ciclos de teste e iteração ao longo do projeto, especialmente em relação à validação de dados e relatórios financeiros, pode evitar problemas de usabilidade e performance no lançamento do sistema. Além disso, testes de carga e performance devem ser incorporados desde o início para garantir que o sistema aguente o volume de dados esperado.


4.	### Documentação e Treinamento
-	Investir mais tempo na documentação detalhada do sistema e em treinamentos para os usuários finais ajudará a garantir uma adoção mais rápida e eficiente. 
5.	### Foco na Integração
-	Para projetos com previsão de integrações externas, como plataformas acadêmicas ou administrativas, é importante considerar esses pontos desde a fase inicial do planejamento. Planejar a arquitetura com modularidade e flexibilidade ajudará na integração futura de sistemas de forma mais eficiente.
________________________________________
## Conclusão
O projeto foi bem-sucedido ao atender aos principais objetivos de otimização de processos no gerenciamento de estoque e controle financeiro. O sistema oferece uma solução prática e escalável para o curso de gastronomia do Senac, permitindo um controle eficiente sobre os insumos alimentícios e seus custos. No entanto, algumas melhorias poderiam ser feitas no planejamento de requisitos, na gestão de mudanças e nos testes de performance. Os aprendizados adquiridos neste projeto serão essenciais para otimizar a execução de futuros projetos, garantindo soluções ainda mais eficazes e ajustadas às necessidades dos usuários.




