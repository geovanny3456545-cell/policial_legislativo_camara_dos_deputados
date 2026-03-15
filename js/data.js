const questions = [
  // ATIVIDADE DE INTELIGÊNCIA - EXISTENTES (BENCHMARK)
  {
    id: 1,
    disciplina: "Atividade de Inteligência",
    topico: "Conceitos de Inteligência",
    enunciado: "A contra-inteligência tem como um de seus objetivos a neutralização da inteligência adversária, visando à proteção de dados e conhecimentos sensíveis.",
    gabarito: "C",
    justificativa: "A contra-inteligência é o ramo da atividade de inteligência que visa prevenir, detectar, obstruir e neutralizar a inteligência adversária e ações de qualquer natureza que constituam ameaça à salvaguarda de dados, informações e conhecimentos de interesse do Estado e da sociedade.",
    fonte: "Existente (Adaptada Cebraspe/ABIN)",
    tipo: "C/E"
  },
  {
    id: 2,
    disciplina: "Atividade de Inteligência",
    topico: "Política Nacional de Inteligência (Decreto 8.793/2016)",
    enunciado: "De acordo com a Política Nacional de Inteligência, a atividade de inteligência no Brasil deve ser pautada pela estrita observância dos direitos e garantias fundamentais previstos na Constituição Federal.",
    gabarito: "C",
    justificativa: "A PNI estabelece que a atividade de inteligência é essencial à segurança do Estado e da sociedade e deve ser exercida com observância aos princípios constitucionais.",
    fonte: "Existente (Benchmark PNI)",
    tipo: "C/E"
  },
  // ATIVIDADE DE INTELIGÊNCIA - INÉDITAS (REVISÃO INTEGRAL)
  {
    id: 3,
    disciplina: "Atividade de Inteligência",
    topico: "Análise de Risco",
    enunciado: "No âmbito da análise de risco, a 'vulnerabilidade' é definida como a fonte externa capaz de causar dano a um ativo, enquanto a 'ameaça' representa a fraqueza interna que pode ser explorada.",
    gabarito: "E",
    justificativa: "Inversão de conceitos. A ameaça é o fator externo (potencial dano), enquanto a vulnerabilidade é a fraqueza interna (ponto de exposição).",
    fonte: "Inédita (Revisão Técnica)",
    tipo: "C/E"
  },
  {
    id: 4,
    disciplina: "Atividade de Inteligência",
    topico: "Segurança da Informação",
    enunciado: "O atributo da 'integridade' na segurança da informação garante que a informação esteja disponível para usuários autorizados sempre que necessário.",
    gabarito: "E",
    justificativa: "O atributo que garante a disponibilidade é a 'Disponibilidade'. A 'Integridade' garante que a informação não foi alterada de forma não autorizada.",
    fonte: "Inédita (Revisão SI)",
    tipo: "C/E"
  },
  // CRIMINOLOGIA - EXISTENTES (BENCHMARK)
  {
    id: 5,
    disciplina: "Criminologia",
    topico: "Objetos da Criminologia",
    enunciado: "A criminologia moderna, influenciada pelo paradigma da reação social, passou a incluir o controle social como um de seus objetos fundamentais de estudo, além do delito, do delinquente e da vítima.",
    gabarito: "C",
    justificativa: "A escola clássica focava no delito. A positivista no delinquente. A criminologia moderna (pós-Segunda Guerra) expandiu o foco para a vítima e para o controle social (instâncias formais e informais).",
    fonte: "Existente (Cebraspe - Diversos)",
    tipo: "C/E"
  },
  // CRIMINOLOGIA - INÉDITAS (REVISÃO INTEGRAL)
  {
    id: 6,
    disciplina: "Criminologia",
    topico: "Prevenção da Infração Penal",
    enunciado: "A prevenção primária foca em atuar sobre o ambiente e grupos de risco antes que o crime ocorra, visando dificultar a oportunidade delitiva por meio de policiamento ostensivo e melhoria da iluminação pública.",
    gabarito: "E",
    justificativa: "A descrição refere-se à prevenção secundária. A prevenção primária atua nas causas estruturais do crime (educação, saúde, moradia), sendo de longo prazo.",
    fonte: "Inédita (Revisão Prevenção)",
    tipo: "C/E"
  }
];

export default questions;
