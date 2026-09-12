title:        Você deve usar o lance que a Amazon sugere?
slug:         usar-o-lance-que-a-amazon-sugere
translation_of: amazon-suggested-bid-and-down-only
summary:      O lance sugerido da Amazon diz o que outros anunciantes pagam. Os seus próprios custos e a sua taxa de conversão de anúncios dizem o que você pode pagar.
categories:   PPC & Advertising
hero_alt:     Um vendedor compara o lance sugerido da Amazon com seu próprio teto calculado
reading_time: 7

Quando você adiciona uma palavra-chave a uma campanha de Sponsored Products, a Amazon mostra um número ao lado dela e chama isso de lance sugerido. A maioria dos vendedores novos usa esse número, porque a tela não oferece alternativa.

Ele é uma leitura do mercado: mais ou menos o que outros anunciantes pagaram por aquela palavra-chave. Ele não sabe nada sobre o seu preço de venda, sobre as suas taxas, sobre o seu custo total de importação (landed cost), nem sobre a frequência com que os cliques dos seus anúncios viram pedidos — e são essas coisas que decidem quanto um clique vale para você.

## O que você vai encontrar neste guia

- O que o lance sugerido e a faixa dele representam
- O máximo que você pode pagar por um clique
- O que as três configurações de lance fazem com o seu lance
- Por que muitos anunciantes preferem down only enquanto estão aprendendo
- Os ajustes por posicionamento, e por que eles são por campanha
- Como testar quanto um clique custa de verdade
- O que o seu lance controla, e o que não controla

## O que é o lance sugerido e o que ele está dizendo a você?

Ele aparece no console de publicidade. Conforme você adiciona palavras-chave ou alvos de produto a uma campanha no Campaign Manager, a Amazon mostra um lance sugerido ao lado de cada um, mais uma faixa de lance sugerido com um limite baixo e um limite alto.

A Amazon descreve essas recomendações como o resultado de analisar um grupo de lances vencedores de anúncios recentes e parecidos dentro da sua categoria, atualizado conforme os lances concorrentes mudam. Elas resumem o que outros pagaram; não preveem o que você vai pagar.

[[A distinção]]
O lance sugerido lê o mercado, não o seu negócio. Todo dado que decide se vale a pena comprar um clique está ausente dele. Dois vendedores que veem a mesma sugestão de $1.35 podem estar certos ao dar lances de $2.00 e $0.40.

[[A armadilha]]
Quando uma palavra-chave não recebe impressões, a faixa convida você a pular para o limite alto dela e parar de pensar. Aí você paga um preço que nunca conferiu contra os seus próprios números.

## Quanto você pode pagar por um clique?

Comece pela contribuição por unidade: o que uma venda deixa depois de todo custo, menos a publicidade. Para um produto importado, isso é o preço de venda menos a taxa de comissão, a taxa de logística do FBA e o custo total de importação da unidade.

Preço de venda | $30.00
Taxa de comissão de 15% | $4.50
Taxa de logística do FBA | $5.80
Custo total de importação por unidade, produto importado | $7.20
Contribuição por unidade antes do gasto com anúncios | $12.50

Esses $12.50 são todo o orçamento de publicidade que uma venda dá a você. A sua taxa de conversão de anúncios é a proporção de cliques de anúncios que viram pedidos atribuídos ao anúncio. A 8%, uma venda leva 12.5 cliques, porque 1 dividido por 0.08 é 12.5.

[[Exemplo prático]]
Contribuição por unidade | $12.50
Taxa de conversão de anúncios | 8%
Cliques por venda, 1 dividido por 0.08 | 12.5
Custo por clique de equilíbrio, $12.50 multiplicado por 8% | $1.00
ACOS de equilíbrio, $12.50 dividido por $30.00 | 41.7%

A $1.00 você não fica com nada, então o ponto de equilíbrio não é o seu teto; é a parede atrás dele. Se a publicidade pode levar metade da contribuição, o seu teto é $0.50 por clique: $6.25 de gasto com anúncios por venda, e $6.25 de lucro.

[[A regra]]
O máximo que você pode pagar por um clique é a contribuição por unidade multiplicada pela taxa de conversão de anúncios. Todo dado é seu, e nenhum deles aparece onde o lance sugerido aparece.

Se em vez disso você pagar a sugestão de $1.35, uma venda custa $1.35 multiplicado por 12.5 cliques, ou seja $16.88 contra $12.50 de contribuição: uma perda de $4.38 por unidade.

Pegue a sua taxa de conversão de anúncios no Campaign Manager: cliques e pedidos atribuídos ao anúncio para o ASIN ao longo de pelo menos 30 dias, o segundo dividido pelo primeiro. Não use unit session percentage do Business Reports do Seller Central, que conta também as sessões orgânicas e descreve o seu listing, não os seus anúncios.

[[O risco]]
Um produto novo não tem taxa de conversão de anúncios medida, e supor uma alta demais infla o seu teto. Produtos com poucas avaliações costumam converter pior, então planeje baixo e troque a suposição quando você tiver algumas centenas de cliques.

## O que as três configurações de lance fazem com o seu lance?

A estratégia de lances é uma configuração da campanha. Ela decide o que a Amazon pode fazer com o seu lance antes de ele entrar em um leilão.

| Configuração | O que a Amazon faz com o lance que você informou | Ela pode aumentar esse lance? |
|---|---|---|
| Dynamic bids - down only (lances dinâmicos, só para baixo) | Reduz o lance em leilões que ela julga menos propensos a converter | Não |
| Dynamic bids - up and down (lances dinâmicos, para cima e para baixo) | Aumenta o lance em leilões que ela julga mais propensos a converter, e reduz nos demais | Sim — a Amazon informa que até 100%, para todos os posicionamentos |
| Fixed bids (lances fixos) | Usa exatamente o lance que você informou | Não |

O limite que a Amazon publica para o up and down são os 100% dessa tabela. Um lance de $0.50 pode, portanto, competir em até $1.00 — o preço de equilíbrio acima, e o dobro do teto que você definiu.

Sob as três, um ajuste por posicionamento ainda pode ser aplicado por cima — uma configuração de campanha separada, explicada abaixo.

[[FIGURE: Um mesmo lance informado virando três lances de leilão diferentes sob as três configurações]]

## Por que muitos anunciantes preferem down only enquanto estão aprendendo?

Porque isso elimina uma incógnita. No up and down, o que você pagou por um clique resulta de duas coisas que você não consegue ver: o que o leilão exigiu, e o quanto a Amazon aumentou o seu lance. Quando o custo volta mais alto do que o esperado, você não consegue dizer qual das duas causou isso.

[[O porquê]]
No down only, o lance que entra no leilão nunca é maior do que o número que você digitou, antes de qualquer ajuste por posicionamento, então o lance que você definiu e o custo que você observou são comparáveis. Enquanto você está aprendendo, essa leitura mais limpa costuma valer mais do que as impressões que o up and down poderia ganhar. É uma preferência, não uma lei: o down only deixa escapar algumas vendas que dava para ganhar.

## O que são os ajustes por posicionamento e por que eles são definidos por campanha?

Os anúncios de Sponsored Products aparecem em três tipos de posição. O topo da busca (primeira página) é a fileira de resultados patrocinados acima dos resultados orgânicos na primeira página de uma busca. O resto da busca é qualquer outra posição patrocinada dentro dos resultados de busca. As páginas de produto são os espaços patrocinados de uma página de detalhes.

A Amazon permite um ajuste de até 900% em cada um, para todos os tipos de segmentação e todas as estratégias de lances. Ele multiplica o lance que você informou, só para aquele posicionamento.

Lance que você informou | $0.50
Ajuste do topo da busca | 50%
Lance que compete no topo da busca, $0.50 multiplicado por 1.50 | $0.75
Lance que compete em todos os outros posicionamentos | $0.50

Agora a campanha compete a $0.75 em um posicionamento, acima do teto que você definiu. Isso pode ser deliberado, mas só se você escolheu.

[[O limite]]
O ajuste pertence à campanha, não à palavra-chave: uma campanha, um conjunto de três percentuais, aplicado a todas as palavras-chave dentro dela. Uma campanha com vinte palavras-chave não consegue dar a nenhuma delas uma estratégia de posicionamento própria. Esse é o argumento prático mais forte a favor de poucas palavras-chave por campanha.

Leia o relatório de posicionamento da Amazon para Sponsored Products antes de definir um ajuste.

## Como você testa quanto um clique custa de verdade?

Às vezes uma palavra-chave devolve quase nenhuma impressão, e esperar não ajuda: um lance abaixo do nível em que o leilão fecha não coleta dado nenhum. O único jeito de descobrir o preço de entrada é aumentar o lance e observar.

[[O que fazer]]
1. Anote a data, a palavra-chave e o lance de onde você está partindo.
2. Coloque essa campanha em down only ou fixed bids, para que o custo que você observar pertença ao lance que você definiu.
3. Limite quanto o teste pode gastar, usando o orçamento diário e uma data de término.
4. Aumente o lance em uma única etapa, não em várias espalhadas por semanas.
5. No fim, leia o custo por clique médio que a Amazon reporta para aquela palavra-chave, devolva o lance ao seu teto e marque as datas do teste nas suas anotações.

Marcar as datas protege os seus dados: o teste infla o custo por clique e o ACOS de propósito, e o lance aumentado pode ganhar cliques em posicionamentos que você normalmente não alcança, então a taxa de conversão daquela janela não é a sua taxa normal.

[[A armadilha]]
As vendas costumam subir durante o teste, porque um lance mais alto compra mais cliques. Isso não é evidência de que ele cabe no seu bolso: cliques acima do seu teto produzem mais vendas e menos lucro ao mesmo tempo.

## O que o seu lance controla de verdade?

Um lance é o máximo que você está disposto a pagar por um clique: um limite que você define, não um preço que você combinou. Ele influencia se você entra no leilão e com que frequência você ganha. A Amazon é explícita que ele não é o único fator, porque a relevância do seu anúncio para a busca do comprador também decide se ele aparece.

[[A confusão]]
O seu lance não define o seu custo por clique. Quem define é o leilão, que é feito dos lances de outros anunciantes, que mudam todo dia e não têm nada a ver com a sua margem. Aumentar um lance de $0.90 para $1.20 não compra um clique de $1.20; compra a permissão de ser cobrado até esse valor.

Então julgue uma palavra-chave pelo custo por clique que a Amazon reporta — gasto dividido pelos cliques — nunca pelo lance que você digitou.

## Perguntas frequentes

**Meu lance era $0.90 e o meu custo por clique reportado é $1.60. Como?**
Confira a estratégia de lances, já que o up and down pode aumentar um lance em até 100%. Depois os ajustes por posicionamento da campanha, que valem sob qualquer estratégia, inclusive o down only. E o número reportado é uma média dos cliques do período, não o preço de um clique.

**E se o meu teto ficar abaixo do lance sugerido?**
Então a palavra-chave provavelmente não cabe no seu bolso hoje. Três coisas movem um teto: um preço de venda mais alto, custos mais baixos e uma taxa de conversão de anúncios melhor.

## Para fechar

O lance sugerido diz a você, rápido e de graça, mais ou menos quanto uma palavra-chave custa para outras pessoas. Ele não consegue dizer se esse é um preço que você deveria pagar.

Existe um jeito de seguir este guia à risca e mesmo assim perder dinheiro. Um teto só está tão atualizado quanto os dois números por trás dele, então se a sua taxa de conversão de anúncios cai, ou se as suas taxas ou o seu custo total de importação sobem, o teto do trimestre passado está alto demais hoje. Recalcule-o por produto sempre que preço, custos ou taxa de conversão mudarem.

Números dos exemplos deste artigo, não de uma pesquisa de mercado.

## New terms

- lance sugerido — o valor que a Amazon exibe ao lado de uma palavra-chave ou alvo de produto quando você o adiciona a uma campanha de Sponsored Products, tirado de lances vencedores recentes de outros anunciantes. Frase do dia a dia: o que outros anunciantes vêm pagando. É uma recomendação: não pode ser traduzido de um jeito que soe como instrução ou exigência.
- faixa de lance sugerido — a banda de mínimo a máximo que a Amazon exibe junto do lance sugerido. Frase do dia a dia: a variação do que outros anunciantes vêm pagando.
- estratégia de lances — a configuração de campanha que decide se a Amazon pode mudar o lance que você informou antes de ele entrar em um leilão. Frase do dia a dia: se a Amazon pode ajustar o seu lance sozinha.
- Dynamic bids - down only / Dynamic bids - up and down / Fixed bids — os três valores dessa configuração, como aparecem no console de publicidade. Ficam em inglês e são glosados uma única vez, na tabela da seção correspondente, para o leitor conseguir casar o texto com a tela. No resto do artigo usam-se as formas curtas down only, up and down e fixed bids, também em inglês.
- ajuste por posicionamento — um percentual que multiplica o seu lance só para um posicionamento, definido na campanha. Frase do dia a dia: pagar mais ou menos dependendo de onde o anúncio aparece.
- posicionamento — já está em GLOSSARIO-PT §3 (placement). Sem mudanças; continua separado de ranqueamento orgânico.
- topo da busca (primeira página) / resto da busca / páginas de produto — os três posicionamentos que a Amazon deixa ajustar separadamente. Frases do dia a dia: a fileira patrocinada acima da primeira página de resultados; as posições patrocinadas no resto da busca; os espaços patrocinados em uma página de detalhes do produto.
- contribuição por unidade — o que sobra de uma venda depois de todo custo, menos a publicidade. Frase do dia a dia: o dinheiro que uma venda dá a você para gastar com anúncios e lucro. Fica distinta de margem, que nunca é usada como substituta aqui.
- custo por clique de equilíbrio — o custo por clique em que a publicidade consome a contribuição por unidade inteira e o lucro é zero. Frase do dia a dia: o preço de clique em que você para de ganhar dinheiro. Usa ponto de equilíbrio, já em GLOSSARIO-PT §3.
- teto — o máximo que um clique pode valer para o leitor, calculado como contribuição por unidade multiplicada pela taxa de conversão de anúncios e definido abaixo do equilíbrio para sobrar lucro. Frase do dia a dia: o lance mais alto que você se permite. NOVO no glossário PT.
- taxa de conversão de anúncios — já está em GLOSSARIO-PT §3 (adicionada 2026-09-12). Pedidos atribuídos ao anúncio divididos pelos cliques, tirados do Campaign Manager. Este artigo se apoia bastante nela, porque sem ela o teto não pode ser calculado. Precisa continuar distinta da taxa de conversão do listing.
- pedido atribuído ao anúncio — já está em GLOSSARIO-PT §3. Sem mudanças.
- unit session percentage — fica em inglês (§2). Aparece SÓ como a métrica que o leitor NÃO deve usar para uma decisão de publicidade, então o contraste com a taxa de conversão de anúncios precisa sobreviver à tradução.
- taxa de comissão — o percentual do preço de venda que a Amazon fica em cada venda (referral fee). Frase do dia a dia: a comissão da Amazon. NOVO no glossário PT; é a forma que o Seller Central brasileiro usa.
- taxa de logística do FBA — a taxa por unidade que a Amazon cobra para separar, embalar e enviar um pedido FBA. NOVO no glossário PT.
- custo total de importação (landed cost) — GLOSSARIO-PT §3 escopa essa forma a artigos cujo produto é importado. O produto do exemplo deste artigo é importado, então a forma de importação é usada no artigo inteiro, com o parêntese em inglês na primeira aparição. PRECISA DE AVAL se o revisor preferir custo total por unidade nas duas frases genéricas (a abertura e o fechamento).
- alvo de produto — o que o inglês chama de product target: o ASIN ou a categoria que você segmenta em uma campanha. NOVO no glossário PT.
- Nenhum rótulo de callout novo. Todos usam rótulos aprovados em GLOSSARIO-PT §6: A distinção, A armadilha, Exemplo prático, A regra, O risco, O porquê, O limite, O que fazer, A confusão.
