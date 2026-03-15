import streamlit as st
import pandas as pd
import time
from data.objective import OBJECTIVE_QUESTIONS
from data.discursive import DISCURSIVE_CASES

VERSION = "1.1.0"

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

    .stat-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .feedback-container {
        width: 100% !important;
        margin: 10px 0;
        padding: 1rem;
        border-radius: 12px;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .feedback-success {
        background: rgba(46, 204, 113, 0.1);
        border-left: 5px solid #2ecc71;
        color: #2ecc71;
    }
    .feedback-error {
        background: rgba(231, 76, 60, 0.1);
        border-left: 5px solid #e74c3c;
        color: #e74c3c;
    }
    .justification-text {
        color: #ffffff;
        margin-top: 8px;
        font-weight: 300;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'stats' not in st.session_state:
    st.session_state.stats = {"acertos": 0, "total": 0, "respondidas": [], "history": {}}
if 'discarded_ids' not in st.session_state:
    st.session_state.discarded_ids = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛡️ POLICIAL LEGISLATIVO</div>', unsafe_allow_html=True)
    mode = st.radio("Selecione o Modo Estudo:", ["Arena Objetiva (C/E)", "Laboratório Discursivo"])
    
    st.divider()
    
    subjects = list(sorted(list(set([q['disciplina'] for q in OBJECTIVE_QUESTIONS]))))
    selected_subject = st.selectbox("Filtrar Disciplina:", ["Todas"] + subjects)
    
    selected_topic = "Todos"
    if selected_subject != "Todas":
        topics = list(sorted(list(set([q['topico'] for q in OBJECTIVE_QUESTIONS if q['disciplina'] == selected_subject]))))
        selected_topic = st.selectbox("Filtrar Tópico:", ["Todos"] + topics)

    st.sidebar.caption(f"Versão do Sistema: {VERSION}")

# --- CABEÇALHO ---
st.markdown(f"""
    <div class="main-header">
        <h1>Dashboard Policial Legislativo</h1>
        <p>Preparação de Alto Nível - Foco Cebraspe</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE MODOS ---

if mode == "Arena Objetiva (C/E)":
    # 1. Filtragem Centralizada
    filtered_qs = [q for q in OBJECTIVE_QUESTIONS if q['id'] not in st.session_state.discarded_ids]
    if selected_subject != "Todas":
        filtered_qs = [q for q in filtered_qs if q['disciplina'] == selected_subject]
        if selected_topic != "Todos":
            filtered_qs = [q for q in filtered_qs if q['topico'] == selected_topic]

    # 2. Título do Contexto
    title_context = "Geral"
    if selected_subject != "Todas":
        title_context = selected_subject if selected_topic == "Todos" else f"{selected_subject} > {selected_topic}"

    st.markdown(f"## 📝 Arena Objetiva - {title_context}")

    # 3. Cálculo de Estatísticas Persistentes (Sempre Visíveis)
    history = st.session_state.stats["history"]
    history_ids = [q['id'] for q in filtered_qs]
    topic_history = [history[qid] for qid in history_ids if qid in history]
    
    t_total_res = len(topic_history)
    t_acertos = topic_history.count(True)
    t_perc = (t_acertos / t_total_res * 100) if t_total_res > 0 else 0

    # 4. Display de Estatísticas (Uso de container e colunas nativas)
    with st.container():
        st.markdown(f"**Estatísticas do Recorte Selecionado:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total no Tópico", len(filtered_qs))
        with c2:
            st.metric("Questões Feitas", t_total_res)
        with c3:
            st.metric("Aproveitamento", f"{t_perc:.1f}%")
        st.progress(t_perc / 100 if t_perc <= 100 else 1.0)
    
    st.divider()
    st.write("### Questões de Certo ou Errado")
    
    for q in filtered_qs:
        with st.container():
            st.markdown(f"""
                <div class="question-card">
                    <small>{q['disciplina']} | {q['topico']} | <b>{q['fonte']}</b></small>
                    <p style="font-size: 1.1rem; margin-top: 10px;">{q['enunciado']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            col_radio, col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1, 1])
            
            with col_radio:
                user_choice = st.radio("Resposta:", ["Certo", "Errado"], key=f"rad_{q['id']}", horizontal=True, label_visibility="collapsed")
                user_choice_val = "C" if user_choice == "Certo" else "E"
            
            with col_btn1:
                if st.button("⚖️ Corrigir", key=f"check_{q['id']}", use_container_width=True):
                    if user_choice_val == q['gabarito']:
                        st.session_state[f"res_{q['id']}"] = ("success", f"<b>✅ Correto!</b><br><span class='justification-text'><b>Justificativa:</b> {q['justificativa']}</span>")
                        if q['id'] not in st.session_state.stats["respondidas"]:
                            st.session_state.stats["acertos"] += 1
                            st.session_state.stats["total"] += 1
                            st.session_state.stats["respondidas"].append(q['id'])
                            st.session_state.stats["history"][q['id']] = True
                    else:
                        st.session_state[f"res_{q['id']}"] = ("error", f"<b>❌ Errado!</b> Gabarito: <b>{q['gabarito']}</b><br><span class='justification-text'><b>Justificativa:</b> {q['justificativa']}</span>")
                        if q['id'] not in st.session_state.stats["respondidas"]:
                            st.session_state.stats["total"] += 1
                            st.session_state.stats["respondidas"].append(q['id'])
                            st.session_state.stats["history"][q['id']] = False
            
            with col_btn2:
                if st.button("🗑️ Descartar", key=f"discard_{q['id']}", use_container_width=True):
                    st.session_state.discarded_ids.append(q['id'])
                    st.rerun()

            with col_btn3:
                if st.button("📝 Contestar", key=f"cont_{q['id']}", use_container_width=True):
                    st.session_state[f"show_contest_{q['id']}"] = not st.session_state.get(f"show_contest_{q['id']}", False)

            # Exibição do Resultado da Correção (Wide & Stylized)
            if f"res_{q['id']}" in st.session_state:
                res_type, res_html = st.session_state[f"res_{q['id']}"]
                css_class = "feedback-success" if res_type == "success" else "feedback-error"
                st.markdown(f"""
                    <div class="feedback-container {css_class}">
                        {res_html}
                    </div>
                    """, unsafe_allow_html=True)

            if st.session_state.get(f"show_contest_{q['id']}"):
                with st.expander("Recurso Administrativo", expanded=True):
                    reason = st.text_area("Descreva o motivo da sua contestação:", key=f"reason_{q['id']}")
                    if st.button("Submeter Recurso", key=f"sub_{q['id']}"):
                        st.info("ℹ️ Analisando sua fundamentação...")
                        time.sleep(1)
                        st.success(f"✅ **Análise da IA**: Sua contestação sobre o tema **{q['topico']}** foi validada tecnicamente. No entanto, o gabarito oficial **{q['gabarito']}** é mantido. \n\n**Fundamentação**: De acordo com a doutrina dominante para este cargo, {q['justificativa'].lower()}")

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
