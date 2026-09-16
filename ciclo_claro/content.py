from __future__ import annotations

from .domain import Phase


PHASE_CONTENT = {
    Phase.MENSTRUACAO: {
        "icon": "●",
        "short": "Menstruação",
        "headline": "Menstruação",
        "feel": "Ela pode estar mais cansada, com cólica, dor de cabeça, sensação de peso ou menor disposição. Também pode estar se sentindo completamente normal.",
        "do": [
            "Pergunte se ela quer ajuda, companhia ou espaço.",
            "Se houver intimidade, ofereça algo concreto: água, comida, descanso ou assumir uma tarefa.",
            "Leve dor e desconforto a sério sem dramatizar.",
        ],
        "avoid": [
            "Atribuir qualquer irritação à menstruação.",
            "Insistir em programa, sexo ou conversa quando ela pedir descanso.",
            "Dar conselho médico sem ser solicitado.",
        ],
        "say": "Quer que eu faça alguma coisa para deixar seu dia mais leve?",
    },
    Phase.FOLICULAR: {
        "icon": "○",
        "short": "Entre fases",
        "headline": "Entre menstruação e ovulação",
        "feel": "Para muitas mulheres esta é uma fase sem sintomas marcantes. Energia e disposição podem estar normais ou aumentando, mas isso varia bastante.",
        "do": [
            "Trate como um dia normal e observe o que ela realmente comunica.",
            "Mantenha atenção e carinho sem procurar sinais escondidos.",
            "Se quiser saber como ela está, pergunte diretamente.",
        ],
        "avoid": [
            "Supor que a fase define humor ou interesse sexual.",
            "Tentar encaixar qualquer comportamento no calendário.",
            "Usar o gráfico como diagnóstico.",
        ],
        "say": "Como você está hoje? Tem algo que eu possa facilitar?",
    },
    Phase.OVULACAO: {
        "icon": "◉",
        "short": "Ovulação",
        "headline": "Ovulação provável",
        "feel": "Muitas mulheres não percebem nenhuma mudança clara. Algumas relatam mais energia, alterações de secreção vaginal, sensibilidade ou leve desconforto pélvico.",
        "do": [
            "Considere a fase apenas como contexto, não como previsão de comportamento.",
            "Pergunte como ela está em vez de presumir desejo, libido ou disposição.",
            "Para contracepção ou fertilidade, use orientação e métodos adequados — não esta estimativa.",
        ],
        "avoid": [
            "Presumir interesse sexual.",
            "Usar o app como método contraceptivo.",
            "Tratar a data estimada como confirmação de ovulação.",
        ],
        "say": "Tem alguma coisa que você queira que eu saiba ou faça hoje?",
    },
    Phase.TPM: {
        "icon": "◐",
        "short": "TPM",
        "headline": "Fase pré-menstrual / TPM possível",
        "feel": "Ela pode estar mais sensível, irritável, ansiosa, cansada, inchada ou com menor tolerância a incômodos. Isso não significa que toda emoção seja 'TPM' — e algumas mulheres quase não têm sintomas.",
        "do": [
            "Escute o conteúdo do que ela diz antes de interpretar o tom.",
            "Ofereça ajuda concreta e aceite se ela preferir espaço.",
            "Em conflitos, mantenha-se nos fatos e evite ironia.",
        ],
        "avoid": [
            "Dizer 'isso é TPM' durante uma discussão.",
            "Invalidar reclamações ou limites.",
            "Esperar o mesmo padrão todos os meses.",
        ],
        "say": "Você quer conversar, quer ajuda com alguma coisa ou prefere um pouco de espaço?",
    },
}

UNKNOWN_TIPS = [
    (
        "Pergunte sem transformar em interrogatório",
        "Se houver intimidade, uma pergunta simples funciona melhor: “Seu ciclo costuma mexer muito com você ou varia bastante?”",
    ),
    (
        "Use o contexto que ela mesma trouxer",
        "Se ela mencionar cólica, cansaço ou que o ciclo está chegando, você pode perguntar: “É algo do ciclo ou é outra coisa?”",
    ),
    (
        "Explique por que quer saber",
        "Uma forma direta e discreta: “Se você se sentir à vontade em me avisar quando estiver numa fase mais chata, eu consigo te apoiar melhor.”",
    ),
]

UNKNOWN_AVOID = (
    "Evite investigar celular, calendário, absorventes, lixo ou mudanças de humor para deduzir a fase. "
    "Discrição aqui significa não pressionar — não descobrir escondido."
)

FLOWER_NAMES = [
    "Jasmim",
    "Camélia",
    "Dália",
    "Íris",
    "Lavanda",
    "Magnólia",
    "Azaleia",
    "Violeta",
]
