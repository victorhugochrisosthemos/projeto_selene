# Ciclo Claro — especificação do MVP mobile v3

## Objetivo

Dar a homens uma leitura rápida e responsável do contexto do ciclo menstrual, priorizando ações práticas e evitando estereótipos.

## Fluxo principal

1. **Entrada mínima:** uma única CTA “Começar”.
2. **O que você sabe agora?**
   - sei a data específica de uma fase;
   - menstruação;
   - TPM;
   - ovulação;
   - não sei.
3. **Não sei:** mostrar apenas orientações discretas e respeitosas para conversar sem investigar escondido.
4. **Dashboard:** após existir contexto suficiente, mostrar:
   - apelido de flor gerado para a sessão;
   - fase atual provável;
   - anel do ciclo;
   - posição aproximada no ciclo;
   - botões para Menstruação, Entre fases, Ovulação e TPM.
5. **Conteúdo de fase:** sempre nesta ordem:
   - o que ela pode estar sentindo;
   - como agir;
   - o que evitar;
   - frase prática opcional.

## UX

- mobile-first;
- sem menu superior com várias páginas;
- uma decisão principal por tela;
- texto curto;
- botões grandes para polegar;
- informações de saúde secundárias ficam recolhidas;
- estimativa e incerteza aparecem sem competir com a ação principal.

## Privacidade no Streamlit Cloud

Esta versão não promete processamento exclusivamente no aparelho. Dados inseridos são transmitidos ao servidor da sessão Streamlit para processamento. O MVP não persiste data, fase ou identidade em SQLite/arquivo e não exige nome, login ou contato.

Para a versão Android final com processamento on-device, migrar a lógica para uma stack nativa/local e usar armazenamento criptografado apenas quando necessário.
