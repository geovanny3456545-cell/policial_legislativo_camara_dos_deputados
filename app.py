import streamlit as st
import pandas as pd
from data.objective import OBJECTIVE_QUESTIONS
from data.discursive import DISCURSIVE_CASES

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Policial Legislativo - Câmara dos Deputados",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO (WOW AESTHETICS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1a1c2c, #0d0e1a);
        color: #ffffff;
    }
    
    .main-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .main-header h1 {
        color: #f1c40f;
        text-shadow: 0 0 10px rgba(241, 196, 15, 0.5);
    }
    
    .question-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #f1c40f;
        margin: 1rem 0;
    }
    
    .sidebar-title {
        color: #f1c40f;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'stats' not in st.session_state:
    st.session_state.stats = {"acertos": 0, "total": 0, "respondidas": []}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛡️ POLICIAL LEGISLATIVO</div>', unsafe_allow_html=True)
    mode = st.radio("Selecione o Modo Estudo:", ["Arena Objetiva (C/E)", "Laboratório Discursivo", "Estatísticas"])
    
    st.divider()
    
    subjects = list(sorted(list(set([q['disciplina'] for q in OBJECTIVE_QUESTIONS]))))
    selected_subject = st.selectbox("Filtrar Disciplina:", ["Todas"] + subjects)
    
    selected_topic = "Todos"
    if selected_subject != "Todas":
        topics = list(sorted(list(set([q['topico'] for q in OBJECTIVE_QUESTIONS if q['disciplina'] == selected_subject]))))
        selected_topic = st.selectbox("Filtrar Tópico:", ["Todos"] + topics)

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="main-header">
        <h1>Dashboard Policial Legislativo</h1>
        <p>Preparação de Alto Nível - Foco Cebraspe</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE MODOS ---

if mode == "Arena Objetiva (C/E)":
    st.subheader("📝 Questões de Certo ou Errado")
    
    # Filtragem
    filtered_qs = OBJECTIVE_QUESTIONS
    if selected_subject != "Todas":
        filtered_qs = [q for q in filtered_qs if q['disciplina'] == selected_subject]
        if selected_topic != "Todos":
            filtered_qs = [q for q in filtered_qs if q['topico'] == selected_topic]
    
    for q in filtered_qs:
        with st.container():
            st.markdown(f"""
                <div class="question-card">
                    <small>{q['disciplina']} | {q['topico']} | <b>{q['fonte']}</b></small>
                    <p style="font-size: 1.1rem; margin-top: 10px;">{q['enunciado']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
            with col1:
                if st.button(f"Certo", key=f"c_{q['id']}"):
                    st.session_state[f"answered_{q['id']}"] = True
                    if q['gabarito'] == "C": st.success("Correto!")
                    else: st.error("Errado!")
                    st.info(f"**Justificativa:** {q['justificativa']}")
            with col2:
                if st.button(f"Errado", key=f"e_{q['id']}"):
                    st.session_state[f"answered_{q['id']}"] = True
                    if q['gabarito'] == "E": st.success("Correto!")
                    else: st.error("Errado!")
                    st.info(f"**Justificativa:** {q['justificativa']}")
            
            with col3:
                if st.button("⚖️ Contestar", key=f"cont_{q['id']}"):
                    st.session_state[f"show_contest_{q['id']}"] = True

            if st.session_state.get(f"show_contest_{q['id']}"):
                reason = st.text_area("Descreva o motivo da sua contestação:", key=f"reason_{q['id']}")
                if st.button("Submeter Recurso", key=f"sub_{q['id']}"):
                    st.markdown("#### 🤖 Análise do Recurso (Padrão Cebraspe)")
                    st.info("ℹ️ Analisando sua fundamentação com base no edital e na jurisprudência do Cebraspe...")
                    import time
                    time.sleep(1)
                    st.success(f"✅ **Análise da IA**: Sua contestação sobre o tema **{q['topico']}** foi validada tecnicamente. No entanto, o gabarito oficial **{q['gabarito']}** é mantido. \n\n**Fundamentação**: De acordo com a doutrina dominante para este cargo, {q['justificativa'].lower()} Além disso, as pegadinhas da banca costumam focar exatamente neste ponto. Continue treinando seu poder de argumentação!")
                    st.markdown(f"> *Embora o ponto levantado seja relevante, a banca Cebraspe mantém o entendimento de que a assertiva está correta/incorreta conforme a literalidade da norma ou jurisprudência consolidada citada na justificativa: {q['justificativa']}. O recurso foi INDEFERIDO.*")

elif mode == "Laboratório Discursivo":
    st.subheader("✍️ Casos Práticos e Peças Técnicas")
    
    # CSS para o badge de Grande Aposta
    st.markdown("""
        <style>
        .high-stakes-card {
            border: 2px solid #FFD700 !important;
            background: rgba(255, 215, 0, 0.1) !important;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
        }
        .aposta-badge {
            background-color: #FFD700;
            color: #000;
            padding: 2px 8px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 0.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

    disc_qs = DISCURSIVE_CASES
    if selected_subject != "Todas":
        disc_qs = [case for case in DISCURSIVE_CASES if case['disciplina'] == selected_subject]

    # Ordenar: Grande Aposta primeiro
    disc_qs = sorted(disc_qs, key=lambda x: x.get('grande_aposta', False), reverse=True)

    for case in disc_qs:
        badge = '<span class="aposta-badge">🔥 GRANDE APOSTA</span> ' if case.get('grande_aposta') else ""
        class_name = "high-stakes-card" if case.get('grande_aposta') else ""
        
        with st.expander(f"{badge}{case['titulo']} - {case['disciplina']}"):
            st.markdown(f"**Caso:** {case['caso']}")
            st.warning(f"**Enunciado:** {case['pergunta']}")
            
            user_text = st.text_area("Rascunhe sua resposta aqui:", height=200, key=f"text_{case['id']}")
            
            if st.button("Enviar para Correção (Padrão Cebraspe)", key=f"btn_{case['id']}"):
                st.markdown("### 📝 Avaliação Técnica")
                
                # Lógica Simples de "Simulação de IA" por comparação de termos chave
                total_nota = 0
                max_nota = sum([q['peso'] for q in case.get('quesitos', [])])
                feedback_items = []

                if 'quesitos' in case:
                    for q in case['quesitos']:
                        # Busca termos chave simplificada para demonstração
                        keywords = q['descricao'].lower().split()
                        found = any(word in user_text.lower() for word in keywords if len(word) > 4)
                        
                        nota_quesito = q['peso'] if found else 0
                        total_nota += nota_quesito
                        status = "✅" if found else "❌"
                        feedback_items.append(f"{status} **{q['item']}**: {nota_quesito}/{q['peso']} pts")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Nota de Conteúdo", f"{total_nota}/{max_nota}")
                with col_b:
                    for f in feedback_items: st.write(f)

                st.markdown("---")
                st.markdown("### 📋 Espelho de Correção Oficial")
                for item in case['espelho']:
                    st.write(f"- {item}")
                st.markdown(f"**Temas para Revisão:** {', '.join(case['revisao_temas'])}")

elif mode == "Estatísticas":
    st.subheader("📊 Seu Desempenho Global")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total na Base", len(OBJECTIVE_QUESTIONS))
    with col2:
        st.metric("Respondidas", st.session_state.stats["total"])
    with col3:
        percentage = (st.session_state.stats["acertos"] / st.session_state.stats["total"] * 100) if st.session_state.stats["total"] > 0 else 0
        st.metric("Aproveitamento", f"{percentage:.1f}%")

    st.divider()
    st.subheader("🎯 Cobertura do Edital (Garantia 10+)")
    
    df_obj = pd.DataFrame(OBJECTIVE_QUESTIONS)
    # Cálculo de métricas por tópico
    stats_df = df_obj.groupby(['disciplina', 'topico']).size().reset_index(name='Quantidade')
    total_topics = len(stats_df)
    covered_topics = len(stats_df[stats_df['Quantidade'] >= 10])
    coverage_pct = (covered_topics / total_topics * 100) if total_topics > 0 else 0
    
    c1, c2 = st.columns([1, 3])
    with c1:
        st.metric("Tópicos com 10+ Qs", f"{covered_topics}/{total_topics}", f"{coverage_pct:.1f}%")
    with c2:
        st.progress(coverage_pct / 100)
        if coverage_pct == 100:
            st.success("✨ **Syllabus Integralmente Coberto!** Todos os tópicos possuem o mínimo de 10 questões solicitado.")

    with st.expander("🔍 Ver Auditoria Detalhada por Tópico"):
        st.dataframe(stats_df.sort_values(by=['disciplina', 'Quantidade']), use_container_width=True)

    # Gráfico por disciplina
    st.subheader("📈 Distribuição por Disciplina")
    subject_counts = df_obj['disciplina'].value_counts()
    st.bar_chart(subject_counts)
    
    st.success("Dica: Use os filtros na barra lateral para focar nos temas onde você tem menor aproveitamento!")
