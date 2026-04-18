---
subject-id: FP451795
subject-name: Foundations of Programming
subject-url: https://fenix.tecnico.ulisboa.pt/disciplinas/FP451795/2017-2018/1-semestre/projetos
tags:
  - FP451795
  - subject
  - projects
---
## 2º Projeto

- Enunciado do SEGUNDO projeto
- Proposta de [solução](https://fenix.tecnico.ulisboa.pt/downloadFile/1407993358860255/parte1.py) do primeiro projeto.
- Foram corrigidas duas gralhas no enunciado (criando um novo enunciado [[projects_proj220171117.pdf]] (originally: [link](https://fenix.tecnico.ulisboa.pt/downloadFile/1689468335597706/proj220171117.pdf)))
  * No primeiro exemplo de interação, está a ser usada a variável `p`. Onde estava pela 1a vez  
>>> p1 = cria_palavra_potencial("META", conjunto)  
devia estar  
>>> p = cria_palavra_potencial("META", conjunto)
  * Foi retirado um ) a mais no exemplo de interação >>> conjunto_palavras_para_cadeia(c)
- É possível usar todas as funções existentes no Pyhton, incluindo bibliotecas.
- **NOVO**: O 2º projecto reutiliza o 1º projecto. Assim, deverá começar com a seguinte linha:
-   * from parte1 import e_palavra


### FAQ 2º Projeto

**1. Em que situações deve ser lançado o erro “cria_palavra_potencial:argumetos invalidos”?**  
O erro deve ser lançado sempre que algum dos elementos do conjunto ou dos caracteres da cadeia de caracteres não são letras maiúsculas.  

**2. O que acontece quando um jogador propõe uma palavra válida que já foi descoberta?**  
O jogo deve reconhecer a proposta como uma palavra válida mas não deve atribuir pontos ao jogador.  

**3. O que acontece quando um jogador introduz uma palavra que não gera uma palavra_potencial?**  
O jogo termina com o erro lançado pelo cria_palavra_potencial.  

**4. Qual a avaliação da instrução subconjunto_por_tamanho(c, 1)?**  
A avaliação da instrução é dependente da representação escolhida para as palavras_potenciais. Em particular, a representação usada na implementação que deu origem ao exemplo está fora do âmbito do presente trabalho, não se esperando que os alunos apresentem a mesma solução. O resultado é obrigatoriamente uma lista de elementos do tipo palavra_potencial. Assim, se a representação interna usada fosse simplesmente uma cadeia de caracteres o resultado da avaliação seria ['A', 'E’]. Se a representação interna usada fosse um tuplo de letras então o resultado seria [(‘A’), (‘E’)].  

**5. Qual a necessidade de definir o TAD palavra_potencial?**  
A palavra_potencial é uma especialização do tipo cadeia de caracteres, permitindo concentrar no TAD a verificação da validade da cadeia.  



**6. Como importar o primeiro projeto?**  
Para que a execução do projeto funcione como esperado no Moonshak, devem incluir a seguinte linha na primeira linha do ficheiro .py a submeter:  
from parte1 import e_palavra  


## 1º Projeto

- [Enunciado do primeiro projeto.](https://fenix.tecnico.ulisboa.pt/downloadFile/845043405456690/proj1.2017_18.20171013.6.pdf)
-   * Nota: No dia 14/10/2017@18:31 foi publicada uma nova versão com pequenas alterações à gramática para ser mais abrangente nas palavras que aceita. Foi ainda acrescentado mais casos de teste ao enunciado.
  * Alterações:
  *     + <silaba3> foi alterado para <silaba_3>
    + Na produção <sílaba_3>, adicionar o símbolo terminal "QUE"
    + Na produção <monossilabo_3>, trocar <par_vogais> por <ditongo>
    + Foi adicionada uma nova regra em <silaba_4>
  * Testes públicos: [fp17proj1publicos.txt](https://fenix.tecnico.ulisboa.pt/downloadFile/563568428757472/fp17proj1publicos.txt)


## Acesso ao sistema Mooshak

A submissão do projecto de FP é feita utilizando o sistema *Mooshak*. Para o poder usar (e assim submeter o projecto) deverá:

- Obter uma password para acesso ao sistema, seguindo as instruções na página: <http://acm.tecnico.ulisboa.pt/~fpshak/cgi-bin/getpass>. A password ser-lhe-á enviada para o email que tem configurado no Fenix. Se a password não lhe chegar de imediato, aguarde.
- Após ter recebido a sua password por email, deve efectuar o login no sistema através da página: <http://acm.tecnico.ulisboa.pt/~fpshak/>. Preencha os campos com a informação fornecida no email.
- Utilize o botão "*Browse...*", seleccione o ficheiro com extensão .py contendo todo o código do seu projecto. O seu ficheiro .py deve conter a implementação das funções pedidas no enunciado. De seguida clique no botão "*Submit*" para efectuar a submissão. Aguarde (10-15 seg) que o sistema processe a sua submissão.
- Quando a submissão tiver sido processada, poderá visualizar na tabela o resultado correspondente. Receberá no seu email um relatório de execução com os detalhes da avaliação automática do seu projecto podendo ver o número de testes passados/falhados.
- Para sair do sistema utilize o botão "*Logout*".
Pontuação: Existem 155 testes configurados no sistema. 15 testes públicos valendo 0 pontos cada (disponíveis no [ficheiro](https://fenix.tecnico.ulisboa.pt/downloadFile/563568428757472/fp17proj1publicos.txt)) e 140 testes privados valendo 10 pontos cada. Como a avaliação automática vale 70% (equivalente a 14 valores) da nota, uma submissão obtém a nota máxima de 1400 pontos.  
Regras: Submeta o seu projecto atempadamente, dado que as restrições seguintes podem não lhe permitir fazê-lo no último momento. Depois dessa de fecho, não serão aceites projectos sob pretexto algum.

- Só poderá efectuar uma nova submissão pelo menos 15 minutos depois da submissão anterior.
- Só são permitidas 10 submissões em simultâneo no sistema, pelo que uma submissão poderá ser recusada se este limite fôr excedido.  
- Não pode ter submissões duplicadas, ou seja submissão igual à anterior.  
- Será considerada para avaliação a última submissão (mesmo que tenha pontuação inferior a submissões anteriores).  
- O sistema fecha às 23:59 do dia 3 de Novembro de 2017.


#### Attachments

- [[projects_proj1.2017_18.20171014.pdf]] (originally: [link](https://fenix.tecnico.ulisboa.pt/downloadFile/845043405456827/proj1.2017_18.20171014.pdf))
- [[projects_proj220171111.pdf]] (originally: [link](https://fenix.tecnico.ulisboa.pt/downloadFile/1407993358860338/proj220171111.pdf))
- [[projects_proj220171117.pdf]] (originally: [link](https://fenix.tecnico.ulisboa.pt/downloadFile/1689468335597706/proj220171117.pdf))
- [FP1718Proj1.pdf](https://fenix.tecnico.ulisboa.pt/downloadFile/1970943312293133/FP1718Proj1.pdf)
- [FP1718P2_AL.pdf](https://fenix.tecnico.ulisboa.pt/downloadFile/1126518382184841/FP1718P2_AL.pdf)

