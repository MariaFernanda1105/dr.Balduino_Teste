"""Conteúdo das páginas de exames dos rins.

Texto educativo em linguagem para pacientes. Os valores de referência são aproximados e variam
entre laboratórios: o texto sempre orienta usar o intervalo impresso no laudo.
IMPORTANTE: revisar com o Dr. Balduino antes da publicação (ver README).
"""


def s(title, body):
    return {"title": title, "body": body}


EXAMS = {
    "creatinina": {
        "title": "Creatinina: o que significa?",
        "lead": "A creatinina é um marcador usado para estimar a função dos rins, mas precisa ser interpretada junto com idade, sexo, massa muscular, hidratação e contexto clínico.",
        "related": ["taxa-de-filtracao-glomerular", "ureia", "proteinuria"],
        "sections": [
            s("O que a creatinina mede",
              "<p>A creatinina é uma substância produzida de forma contínua pelos músculos do corpo. Ela cai na corrente sanguínea e é eliminada quase totalmente pelos rins, na urina. Quando a filtração dos rins diminui, a creatinina deixa de ser eliminada na mesma velocidade e passa a se acumular no sangue.</p>"
              "<p>Por isso, a dosagem de creatinina no sangue é um dos exames mais usados para avaliar a função renal. Mas ela é um marcador indireto: o que ela mostra depende de quanta creatinina o corpo produz e de quanto os rins conseguem eliminar.</p>"),
            s("Valores de referência",
              "<p>Em adultos, os laboratórios costumam apresentar valores de referência entre aproximadamente 0,6 e 1,3 mg/dL. Homens tendem a ter valores mais altos que mulheres, porque têm, em média, mais massa muscular. Cada laboratório define seu próprio intervalo, e é ele que deve ser considerado na leitura do laudo.</p>"
              "<p>Um valor dentro da referência nem sempre significa que os rins estão normais. Pessoas idosas ou com pouca massa muscular podem ter perda importante de função renal com creatinina aparentemente normal. Por isso, a creatinina é usada para calcular a taxa de filtração glomerular (TFG), que é mais informativa.</p>"),
            s("Por que pode estar alterada",
              "<p>A creatinina pode se elevar por motivos que não são doença renal crônica, como desidratação, exercício físico intenso, grande massa muscular, uso de suplementos de creatina e consumo muito elevado de carne. Alguns medicamentos, como certos antibióticos e anti-inflamatórios, também podem alterar o resultado ou reduzir temporariamente a filtração.</p>"
              "<p>Também há causas renais, como lesão renal aguda, doença renal crônica, obstrução urinária e doenças dos glomérulos. Entender qual é o caso exige comparar com exames anteriores e avaliar o conjunto clínico.</p>"),
            s("Quando se preocupar",
              "<p>Merecem avaliação a creatinina que aumenta em relação aos exames anteriores, que permanece elevada em exames repetidos ou que vem acompanhada de proteína na urina, pressão alta, inchaço, alteração no volume da urina ou TFG reduzida.</p>"
              "<p>Um valor isolado, sem comparação, raramente define um diagnóstico. Leve os exames anteriores e a lista de medicamentos à consulta e não suspenda nenhum remédio por conta própria.</p>"),
        ],
    },
    "taxa-de-filtracao-glomerular": {
        "title": "Taxa de filtração glomerular: o que é?",
        "lead": "A TFG é uma estimativa de quanto os rins filtram por minuto. Ela ajuda a classificar a função renal, mas não deve ser analisada isoladamente.",
        "related": ["creatinina", "albuminuria", "ureia"],
        "sections": [
            s("O que é a TFG",
              "<p>Os rins filtram o sangue em pequenas estruturas chamadas glomérulos. A taxa de filtração glomerular (TFG) expressa quanto sangue é filtrado por minuto e é considerada a melhor medida geral da função dos rins.</p>"
              "<p>Na prática, a TFG não é medida diretamente: ela é estimada por uma fórmula, como a CKD-EPI, que usa o valor da creatinina, a idade e o sexo. Muitos laboratórios já informam a TFG estimada no próprio laudo, em mL/min/1,73 m².</p>"),
            s("Como interpretar os valores",
              "<p>De forma geral, a TFG é classificada em estágios: G1 (90 ou mais), G2 (60 a 89), G3a (45 a 59), G3b (30 a 44), G4 (15 a 29) e G5 (menos de 15). A TFG tende a diminuir lentamente com o envelhecimento, e um valor entre 60 e 89 pode ser esperado em pessoas idosas sem doença renal.</p>"
              "<p>O diagnóstico de doença renal crônica não depende só de um número: considera uma TFG abaixo de 60 por mais de três meses ou outros sinais de lesão renal, como albuminúria. O estágio também é analisado junto com a quantidade de albumina na urina.</p>"),
            s("Limitações do cálculo",
              "<p>Como a fórmula depende da creatinina, a TFG estimada pode ser menos precisa em pessoas com massa muscular muito diferente da média, em dietas especiais, em gestação, em obesidade importante e durante doenças agudas. Em situações selecionadas, o médico pode pedir outros exames, como a cistatina C ou uma medida da depuração de creatinina.</p>"),
            s("Quando se preocupar",
              "<p>Valores abaixo de 60 mL/min/1,73 m² que persistem, quedas rápidas em relação a exames anteriores ou uma TFG reduzida acompanhada de proteína ou sangue na urina merecem avaliação especializada. O acompanhamento ao longo do tempo costuma ser mais importante do que um resultado isolado.</p>"),
        ],
    },
    "proteinuria": {
        "title": "Proteinúria: quando é preocupante?",
        "lead": "A presença de proteínas na urina pode ser transitória ou sinalizar doença renal. Persistência, quantidade e tipo de proteína orientam a investigação.",
        "related": ["albuminuria", "hematuria", "taxa-de-filtracao-glomerular"],
        "sections": [
            s("O que é proteinúria",
              "<p>Proteinúria significa a presença de proteínas na urina. Em condições normais, os rins filtram o sangue e deixam passar apenas quantidades mínimas de proteína. Quando a barreira de filtração dos glomérulos é lesionada, mais proteína escapa para a urina.</p>"
              "<p>Um sinal que algumas pessoas relatam é a urina com muita espuma, mas esse sinal é inespecífico: a espuma pode ter outras causas, e a proteinúria muitas vezes não provoca nenhum sintoma visível.</p>"),
            s("Como é medida",
              "<p>A proteína pode aparecer na fita do exame de urina (EAS) com cruzes (+, ++, +++), mas esse resultado é apenas qualitativo. Para quantificar, usa-se a proteinúria de 24 horas ou, com mais praticidade, a relação proteína/creatinina em uma amostra isolada de urina.</p>"
              "<p>Como referência aproximada, a excreção normal é inferior a cerca de 150 mg por dia. Os valores exatos e o método dependem do laboratório.</p>"),
            s("Causas transitórias e persistentes",
              "<p>A proteinúria pode ser passageira em situações como febre, exercício intenso, desidratação, infecção urinária e, em alguns jovens, ao ficar muito tempo em pé. Quando persiste em exames repetidos, pode estar associada a diabetes, hipertensão, glomerulopatias e outras doenças renais.</p>"),
            s("Quando se preocupar",
              "<p>É importante investigar quando a proteína persiste em mais de uma amostra, quando a quantidade é elevada ou quando há sangue na urina, inchaço, pressão alta ou queda da TFG. Quantidades muito altas (em torno de 3 a 3,5 g por dia ou mais) podem fazer parte de um quadro chamado síndrome nefrótica, que exige avaliação especializada.</p>"
              "<p>Proteína na urina não é um diagnóstico: é um sinal que precisa ser confirmado, quantificado e interpretado em conjunto com a história clínica.</p>"),
        ],
    },
    "albuminuria": {
        "title": "Albuminúria: por que medir?",
        "lead": "A albuminúria detecta a perda de albumina pela urina e pode identificar risco renal precoce, especialmente em pessoas com diabetes ou hipertensão.",
        "related": ["proteinuria", "taxa-de-filtracao-glomerular", "creatinina"],
        "sections": [
            s("O que é albuminúria",
              "<p>A albumina é a principal proteína do sangue. Quando os rins começam a ser lesionados, ela é uma das primeiras a aparecer na urina, muitas vezes antes de qualquer mudança na creatinina ou na TFG. Por isso, a albuminúria é considerada um marcador sensível de lesão renal precoce e também de risco cardiovascular.</p>"),
            s("Como é feito o exame",
              "<p>O exame mais usado é a relação albumina/creatinina (RAC) em uma amostra isolada de urina, preferencialmente a primeira da manhã. A urina de 24 horas também pode ser usada, mas é mais trabalhosa e sujeita a erros de coleta.</p>"
              "<p>Como o resultado pode variar de um dia para outro, uma alteração costuma precisar ser confirmada em novas amostras ao longo de alguns meses.</p>"),
            s("Como interpretar",
              "<p>De forma geral, a RAC é classificada em A1 (menor que 30 mg/g, normal ou discretamente aumentada), A2 (30 a 300 mg/g, moderadamente aumentada) e A3 (maior que 300 mg/g, muito aumentada). Essa classificação é combinada com a TFG para estimar o risco e definir a frequência do acompanhamento.</p>"
              "<p>Exercício intenso, febre, infecção urinária, descompensação do diabetes e menstruação podem elevar o resultado temporariamente.</p>"),
            s("Quem deve fazer e quando se preocupar",
              "<p>Pessoas com diabetes, hipertensão, doença cardiovascular ou histórico familiar de doença renal costumam ser orientadas a medir a albuminúria periodicamente, geralmente uma vez por ano, ou conforme a indicação médica. Valores persistentemente acima de 30 mg/g merecem avaliação, mesmo quando a creatinina está normal.</p>"),
        ],
    },
    "hematuria": {
        "title": "Hematúria: sangue na urina",
        "lead": "Sangue na urina pode ter causas diversas. Quando persiste ou aparece com outros achados, precisa ser investigado com atenção.",
        "related": ["proteinuria", "ultrassonografia-dos-rins", "creatinina"],
        "sections": [
            s("O que é hematúria",
              "<p>Hematúria é a presença de hemácias (glóbulos vermelhos) na urina. Pode ser macroscópica, quando a urina fica avermelhada, rosada ou cor de chá, ou microscópica, quando só é detectada no exame de urina (EAS). Na hematúria microscópica, o laudo costuma indicar a quantidade de hemácias por campo, e valores acima de cerca de 3 por campo são geralmente considerados alterados, conforme o laboratório.</p>"),
            s("Possíveis causas",
              "<p>As causas são variadas: infecções urinárias, cálculos renais, exercício físico intenso, coleta durante a menstruação, medicamentos que afetam a coagulação, doenças da próstata, alterações das vias urinárias e doenças dos glomérulos. Em alguns casos, a causa não é encontrada ou é benigna.</p>"
              "<p>Uma das primeiras perguntas é se o sangue vem dos glomérulos (hematúria glomerular, mais ligada ao nefrologista) ou das vias urinárias (mais ligada ao urologista). Sinais como hemácias deformadas, cilindros hemáticos e proteinúria associada sugerem origem glomerular.</p>"),
            s("Como é a investigação",
              "<p>Em geral, começa pela repetição do exame de urina, pela análise do sedimento, por exames de sangue (creatinina, TFG), pela medida da proteinúria ou da albuminúria e por exames de imagem, como a ultrassonografia. Dependendo da idade e dos fatores de risco, como tabagismo, pode ser necessária avaliação conjunta com o urologista.</p>"),
            s("Quando se preocupar",
              "<p>A urina visivelmente com sangue deve sempre ser avaliada. Também merecem atenção a hematúria que persiste em exames repetidos, a que vem com proteinúria, hipertensão ou inchaço, e a que se acompanha de dor, febre ou dificuldade para urinar. Em situações de dor intensa, febre alta ou impossibilidade de urinar, procure um serviço de urgência.</p>"),
        ],
    },
    "ureia": {
        "title": "Ureia: o que esse exame avalia?",
        "lead": "A ureia participa da avaliação clínica, mas varia com hidratação, alimentação, sangramentos e outras condições. Seu resultado deve ser contextualizado.",
        "related": ["creatinina", "taxa-de-filtracao-glomerular", "proteinuria"],
        "sections": [
            s("O que a ureia mede",
              "<p>A ureia é produzida no fígado a partir da degradação das proteínas e é eliminada principalmente pelos rins. Quando a função renal diminui, a ureia tende a se acumular no sangue. Por isso, ela é usada, junto com a creatinina, na avaliação da função dos rins.</p>"),
            s("Valores de referência",
              "<p>Em adultos, os valores de referência costumam ficar entre aproximadamente 15 e 45 mg/dL, com variação entre laboratórios. Considere sempre o intervalo informado no seu laudo.</p>"),
            s("Por que a ureia varia tanto",
              "<p>A ureia é menos específica que a creatinina. Ela pode subir com desidratação, dieta muito rica em proteínas, sangramento no aparelho digestivo, uso de corticoides, febre, insuficiência cardíaca e em pessoas idosas. Pode ficar baixa em dietas pobres em proteínas e em algumas doenças do fígado.</p>"
              "<p>A relação entre ureia e creatinina também ajuda o médico a distinguir, por exemplo, uma redução da função renal por falta de líquidos de uma causada por doença dos próprios rins.</p>"),
            s("Quando se preocupar",
              "<p>Ureia elevada acompanhada de creatinina alterada, TFG reduzida ou sintomas como náuseas, cansaço, coceira, inchaço ou redução do volume da urina precisa de avaliação. Valores muito elevados, com sintomas importantes, podem exigir atendimento de urgência.</p>"),
        ],
    },
    "ultrassonografia-dos-rins": {
        "title": "Ultrassonografia dos rins: o que podemos encontrar?",
        "lead": "O exame pode mostrar tamanho, posição, dilatação, cistos e cálculos, mas seus achados devem ser relacionados aos sintomas e exames laboratoriais.",
        "related": ["hematuria", "creatinina", "biopsia-renal"],
        "sections": [
            s("O que é e como é feito",
              "<p>A ultrassonografia dos rins e das vias urinárias usa ondas sonoras para formar imagens, sem radiação e sem contraste. É indolor e costuma levar poucos minutos. O preparo varia conforme o serviço, mas geralmente pede a bexiga cheia e, às vezes, jejum. Siga a orientação do local onde o exame será feito.</p>"),
            s("O que o exame avalia",
              "<p>O exame mostra o tamanho e a forma dos rins (em adultos, o comprimento costuma ficar em torno de 9 a 12 cm), a espessura do tecido renal, a diferença entre os dois lados, a presença de cistos, cálculos, dilatação das vias urinárias (hidronefrose), massas e o aspecto da bexiga.</p>"
              "<p>Rins diminuídos e com brilho aumentado (ecogenicidade aumentada) podem sugerir doença renal crônica de longa duração. Cistos simples são muito comuns, em geral benignos e, na maioria das vezes, não precisam de tratamento.</p>"),
            s("O que o exame não mostra",
              "<p>A ultrassonografia avalia a estrutura dos rins, não a função. Um exame normal não exclui doença dos glomérulos, e cálculos muito pequenos podem não ser identificados. Por isso, o resultado é sempre interpretado junto com exames de sangue e de urina.</p>"),
            s("Quando se preocupar",
              "<p>Termos como hidronefrose, afilamento do parênquima, ecogenicidade aumentada, assimetria importante entre os rins ou nódulo/massa merecem avaliação médica. Já achados como cistos simples pequenos costumam ser apenas acompanhados. Leve o laudo e as imagens à consulta para uma interpretação adequada.</p>"),
        ],
    },
    "biopsia-renal": {
        "title": "Quando é necessária uma biópsia renal?",
        "lead": "A biópsia pode ser indicada em situações selecionadas para esclarecer a causa de alterações renais e orientar o tratamento. A decisão é individualizada.",
        "related": ["proteinuria", "hematuria", "ultrassonografia-dos-rins"],
        "sections": [
            s("O que é a biópsia renal",
              "<p>A biópsia renal consiste na retirada de um pequeno fragmento do tecido do rim, com uma agulha fina, para análise em laboratório. O tecido é examinado em microscopia de luz, imunofluorescência e, em alguns casos, microscopia eletrônica. É o exame que permite identificar com precisão o tipo de doença que afeta os glomérulos e outras estruturas.</p>"),
            s("Quando pode ser indicada",
              "<p>A biópsia costuma ser considerada quando há proteinúria importante ou síndrome nefrótica sem causa clara, hematúria de origem glomerular com proteinúria, perda de função renal sem explicação, suspeita de doenças que afetam os rins, como o lúpus, e em alguns casos de rim transplantado. Nem toda alteração na urina precisa de biópsia: a indicação depende do conjunto de achados e do quanto o resultado pode mudar o tratamento.</p>"),
            s("Como é feita",
              "<p>O procedimento é feito com anestesia local, geralmente guiado por ultrassonografia. Antes, são avaliados a pressão arterial, os exames de coagulação e o uso de medicamentos que afetam o sangramento, que podem precisar ser suspensos apenas sob orientação médica. Após o procedimento, a pessoa permanece em observação por algumas horas, e em alguns serviços por até 24 horas.</p>"),
            s("Riscos e cuidados",
              "<p>O principal risco é o sangramento, que pode causar sangue na urina ou um hematoma ao redor do rim. Na grande maioria dos casos, ele é leve, mas complicações maiores podem ocorrer raramente e exigir outros procedimentos. Pressão alta mal controlada, distúrbios de coagulação, rim único e rins muito pequenos podem aumentar o risco ou contraindicar o exame.</p>"
              "<p>O resultado costuma levar alguns dias e ajuda a definir o diagnóstico, o prognóstico e o tratamento. A decisão de realizar a biópsia deve ser conversada com o nefrologista, pesando benefícios e riscos em cada caso.</p>"),
        ],
    },
}
