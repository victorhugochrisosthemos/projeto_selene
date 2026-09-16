# Ciclo Claro — mobile MVP v3

MVP em Streamlit com fluxo mobile-first:

1. Tela inicial mínima.
2. Seleção do que o usuário sabe: data específica, menstruação, TPM, ovulação ou “não sei”.
3. Se “não sei”, orientações discretas e respeitosas para conversar sem investigar escondido.
4. Após definir uma fase, dashboard com apelido de flor, gráfico do ciclo e conteúdo clicável por fase.

## Rodar localmente

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

Suba a pasta para um repositório GitHub e configure `app.py` como arquivo principal.

### Privacidade importante

Em Streamlit Cloud, entradas do usuário são transmitidas ao servidor que executa a sessão. Por isso esta versão **não promete processamento exclusivamente no aparelho**. O app foi desenhado para não persistir datas/fases em banco ou arquivo; o contexto fica apenas na sessão em memória.

Para uma futura versão Android com a promessa literal “nenhum dado do ciclo sai do aparelho”, a lógica deve migrar para processamento on-device (por exemplo, Kotlin/Compose + Room/Keystore ou Flutter + armazenamento local criptografado).

## Conteúdo de saúde

O app é educacional. Estimativas de calendário não confirmam ovulação, fertilidade, gravidez ou condições médicas e não devem ser usadas como método contraceptivo.


## Streamlit Cloud no celular

A interface remove via CSS o header, toolbar, padding superior e badges conhecidos do Streamlit. Para a apresentação mais limpa suportada oficialmente pelo Streamlit, abra o endereço público acrescentando `?embed=true`, por exemplo: `https://SEU-APP.streamlit.app/?embed=true`. Esse modo remove toolbar, padding superior/inferior, footer e a linha colorida do Streamlit.

A barra de endereço do Chrome/Safari pertence ao navegador e não pode ser removida por CSS do Streamlit. Para experiência sem barra do navegador é necessário instalar/empacotar o produto como PWA/app Android (WebView/TWA).


## Correção mobile v5

Esta versão remove explicitamente o header/top padding do Streamlit em telas móveis usando três camadas: CSS normal com `.stMainBlockContainer`, CSS persistente inserido no `<head>` e reaplicação por `MutationObserver` após reruns. Isso ataca o espaço branco que pode aparecer no Chrome Android em apps não embedded.

Para validar depois do deploy, feche a aba antiga e abra o app novamente (ou use uma aba anônima) para evitar CSS antigo em cache.
