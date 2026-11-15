# Relatório da revisão final do site IVAN

Data: 15/11/2026. Site revisado: https://yaka04.github.io/ivanbr-site/ (versões `/`, `/en/` e `/zh/`; `/pt/` também funciona e leva à versão em português).

Base das correções: a apresentação institucional do cliente (texto em chinês e inglês). Nada foi acrescentado além do que está nela.

---

## 1. Correções em português

- **Apresentação institucional:** a IVAN INTERNATIONAL TRADER GROUP LTDA agora é descrita como "empresa constituída no Brasil e investida pela IVAN International Trade Group Limited, sediada em Hong Kong". É a tradução de "investee company" usada no documento original. O site não diz que o grupo é brasileiro.
- **Topo da página:** "Somos a empresa brasileira vinculada ao grupo IVAN, sediado em Hong Kong."
- **Seção da empresa:** novo título ("Empresa constituída no Brasil, vinculada a um grupo de Hong Kong"). O campo "Grupo" virou "Empresa investidora".
- **Experiência internacional:** a antiga seção "Clientes de referência" agora se chama "Experiência internacional", com o subtítulo "Relacionamento com empresas de destaque nos setores de PCB e PCBA em diferentes mercados". A página não traz avisos nem afirma que as empresas são clientes atuais. No menu, o item virou "Experiência".
- **Linha do tempo, 2012–2026:** "Fornecimento para…" virou "Expansão para fabricantes de PCB em diferentes mercados…", que não afirma vendas.
- **MAX600:** "Repetibilidade" foi trocada por "Precisão da profundidade de aplicação do anel" e "Precisão de detecção do diâmetro externo", como no documento em inglês.
- **Fichas técnicas:** cada uma ganhou a linha "Designação do fabricante", com o nome oficial em inglês.
- **Fotos:** os textos alternativos agora começam com "Foto:" seguido do nome do equipamento.

## 2. Correções em inglês

- **About:** "IVAN INTERNATIONAL TRADER GROUP LTDA is a company incorporated in Brazil and an investee company of IVAN International Trade Group Limited, headquartered in Hong Kong." O texto segue o documento original.
- **Topo da página:** "We are the Brazilian company affiliated with the IVAN group, headquartered in Hong Kong."
- **International Experience:** o subtítulo é "Relationships with companies across the PCB and PCBA industries in different markets". No menu, o item virou "Experience".
- **MAX600:** "Ring loading depth accuracy" e "Outer diameter detection accuracy", como no documento.
- **PTH:** "horizontal PTH electroless copper (deposition) line services", como no documento. O site não fala em "electrolytic".
- **Nomes dos equipamentos:** os títulos usam termos naturais do setor, como "regrinding", "re-marking" e "ring setting". O nome original do fabricante (por exemplo, "Change Mark Machine") aparece na primeira linha de cada ficha técnica.

## 3. Correções em chinês

- **公司简介:** usa a formulação do documento original: "为香港 IVAN International Trade Group Limited 在巴西的投资主体"; "依托香港 IVAN 的中国供应链与技术服务资源，双方共同开拓巴西及南美市场".
- **首屏文案:** "在巴西的运营公司" foi trocado por "在巴西的投资主体", o termo do original.
- **国际经验:** "客户代表" virou "国际经验", com o subtítulo "与多个市场的 PCB 及 PCBA 领域知名企业建立了业务往来"; no menu também aparece "国际经验".
- **MAX-500:** a descrição voltou ao texto original completo (补偿"大小头""重叠分离"参数，自动调整套环高度).
- **发展历程 2012–2026:** "设备销往…" virou "业务拓展至…".
- **Nomenclatura:** os nomes dos equipamentos e das especificações seguem o original do fabricante (全自动钻针研磨机、钻针清洗机、钻针换标机、清洗换标机、微钻全自动上环机、套环环深重复精度 etc.).
- **Título da seção da empresa:** foi reescrito para não quebrar no meio de uma palavra no celular.

## 4. Melhorias visuais

- **Fichas técnicas:** a primeira linha agora mostra a designação do fabricante, e as linhas continuam com fundo alternado.
- **Título em chinês:** a seção da empresa ganhou uma quebra de linha controlada.
- **Mantido desde a revisão anterior:** cabeçalho de 56 px no celular, seletor de idioma com sigla, blocos PCB/PCBA, fotos sem corte, linha do tempo em verde e lista de referências por região. A identidade visual não mudou.

## 5. Funcionalidades testadas

Os testes foram automatizados e feitos no computador (1440 px) e no celular (390 px), nas três versões, simulando o endereço do GitHub Pages. Resultado: **95 de 95 aprovados**.

| Teste | Resultado |
|---|---|
| Idioma correto em cada página | OK |
| Todas as imagens carregam | OK |
| Fonte carregada | OK |
| Sem rolagem lateral e sem texto cortado | OK |
| Links internos e âncoras (16 por página) com destino | OK |
| 5 fichas técnicas abrem e fecham | OK |
| 5 botões "Pedir orçamento" com o nome do equipamento na mensagem | OK |
| Todos os links de WhatsApp para +55 11 95849-6113 | OK |
| Formulário abre o WhatsApp com nome, empresa, interesse e mensagem | OK |
| Formulário vazio não abre o WhatsApp | OK |
| Troca de idioma mantém a seção (ex.: PT `#a02` → EN `#a02`) | OK |
| Troca de idioma no topo vai para o início | OK |
| `/pt/#a03` leva à versão em português na mesma seção | OK |
| Menu do celular: idiomas visíveis, link leva à seção e fecha o menu | OK |
| Designação do fabricante nas 5 fichas, nos 3 idiomas | OK |
| Textos alternativos em todas as imagens | OK |
| Página 404 com estilo e link para o início, no subcaminho do GitHub Pages | OK |
| Nenhum erro de JavaScript e nenhum arquivo faltando | OK |

**Site publicado:** a versão anterior está no ar em yaka04.github.io/ivanbr-site/ e carrega normalmente. A versão nova só vai aparecer depois de enviar os arquivos (seção 9).

## 6. Mantido sem alteração por falta de confirmação

- **MAX-500, alimentação:** "220 VAC, 50/60 Hz (400 W/H)", como no documento. A unidade "W/H" não foi corrigida.
- **MAX-500, parâmetros:** "cabeça grande / cabeça pequena" e "sobreposição / separação" ("large-head / small-head", "overlap / separation"). Na literatura do setor, o par "overlap / gap" aparece como classe de defeito na inspeção AOI, mas o termo do fabricante foi mantido.
- **MAX600 em chinês:** o original usa "重复精度" (repetibilidade), e o inglês do mesmo documento usa "accuracy" (precisão). Cada idioma manteve o termo do próprio documento.
- **PTH:** "deposição química de cobre" / "electroless copper". O site não fala em "cobre eletrolítico".
- **Nomes das empresas de referência:** estão como no documento, inclusive "Eliant" (依顿) e "Shenzhen Jincheng Precision Technology" (金洲).
- **Endereço:** "Condomínio Portal Anhangueira", como no documento.
- **Domínio:** nenhum está configurado. O site não cita ivanbr.com.br, ivanpcb.com.br nem ivangroup.com.br como endereço ativo.

## 7. Perguntas para o cliente

1. **MAX-500, consumo:** o "400 W/H" é potência de 400 W? Qual unidade devemos publicar?
2. **MAX-500, parâmetros:** qual é a nomenclatura oficial de "大小头" e "重叠分离" em inglês e português?
3. **MAX600:** a especificação é precisão ou repetibilidade (o "重复精度" do chinês)?
4. **MAX600, nome comercial:** em português, preferem "aplicação de anéis" ou outro termo?
5. **Linha PTH:** qual é o nome comercial correto da linha horizontal de PTH (deposição química de cobre)?
6. **Empresas de referência:** podemos manter a lista? Algum nome deve sair? 依顿 é "Ellington Electronics"? 金洲 é "Jinzhou Precision"?
7. **Endereço:** o correto é "Portal Anhangueira" ou "Portal Anhanguera"?
8. **Contato:** o +55 11 95849-6113 atende pelo WhatsApp? Existe e-mail para publicar?
9. **Logo:** existe logotipo oficial?
10. **Domínio:** qual será o definitivo, ivanpcb.com.br ou ivangroup.com.br?

## 8. Arquivos modificados

- `content.py`: textos dos três idiomas, nomes do fabricante (`MAKER_NAMES`) e exemplos de domínio
- `build.py`: linha de designação do fabricante, textos alternativos, página `/pt/` e quebra de linha no título da empresa
- `README.md`: instruções de domínio e lista de pendências
- `RELATORIO-REVISAO.md`: este relatório (novo)
- `docs/` inteira: gerada de novo (`index.html`, `en/index.html`, `zh/index.html`, `pt/index.html` nova, `404.html`)

## 9. Como publicar a versão atualizada

1. Abra o repositório **github.com/yAka04/ivanbr-site**.
2. Clique em **Add file → Upload files**.
3. Da pasta `ivanbr-site` no seu PC, arraste as pastas `docs` e `src` e os arquivos `build.py`, `content.py`, `README.md` e `RELATORIO-REVISAO.md`. O GitHub substitui os arquivos que já existem.
4. Clique em **Commit changes**.
5. Em um ou dois minutos, a nova versão aparece em https://yaka04.github.io/ivanbr-site/ (acompanhe a bolinha na aba **Actions**).

**Quando o domínio for registrado:**
1. Configure o DNS conforme o README.
2. Preencha `SITE_URL` e `CUSTOM_DOMAIN` em `content.py` e rode `python3 build.py`.
3. Envie a pasta `docs` de novo e marque **Enforce HTTPS** em Settings → Pages.
