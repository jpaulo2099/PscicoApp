import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Glauco App - Fluxo Progressivo",
    page_icon="🧠",
    layout="centered"
)

# --- CSS AVANÇADO + ANIMAÇÃO ---
st.markdown("""
    <style>
    /* Fundo Geral */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ANIMAÇÃO DE ENTRADA (FADE IN) */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Aplica a animação aos Cards */
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border: 1px solid #eef0f2;
        animation: fadeIn 0.8s ease-out; /* Efeito de surgimento */
    }
    
    /* Títulos das Seções */
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 15px;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
    }
    
    /* Estilo dos Cards de Necessidade e Emoção */
    .need-tag {
        background-color: #f1f3f5;
        border-left: 4px solid #adb5bd;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        color: #495057;
        font-size: 0.95rem;
    }
    .emotion-tag {
        background-color: #fff4e6;
        border-left: 4px solid #ffc078;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 8px;
        color: #d9480f;
    }
    
    /* Resultado da Díade */
    .result-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 100%);
        color: #1565c0;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS (Baseado na Fonte 17) ---
necessidades_db = {
    "Presença emocional consistente": "Sentir-se seguro, protegido e não abandonado",
    "Proteção física e emocional": "Sentir-se seguro, protegido e não abandonado",
    "Previsibilidade relacional": "Sentir-se seguro, protegido e não abandonado",
    "Responsividade às necessidades": "Sentir-se seguro, protegido e não abandonado",
    "Continuidade do vínculo": "Sentir-se seguro, protegido e não abandonado",
    "Escuta genuína": "Ser visto e compreendido emocionalmente",
    "Reconhecimento dos sentimentos": "Ser visto e compreendido emocionalmente",
    "Legitimação da experiência": "Ser visto e compreendido emocionalmente",
    "Consolo diante da dor": "Ser visto e compreendido emocionalmente",
    "Aceitação das imperfeições": "Sentir-se digno de amor como se é",
    "Afeto não condicionado": "Sentir-se digno de amor como se é",
    "Incentivo à independência": "Sentir-se capaz de agir por conta própria",
    "Feedback realista": "Sentir-se eficaz e capaz",
    "Limites psicológicos claros": "Desenvolver um 'eu' próprio",
    "Poder dizer 'não'": "Poder expressar o que sente e precisa",
    "Brincar / Humor": "Viver com leveza, jogo e vitalidade",
    "Regras claras": "Aprender limites seguros e consistentes",
    "Rotina / Estabilidade": "Sentir que o mundo é compreensível e confiável"
}

impulses_db = {
    "Alegria": "Desejo de reproduzir mais vezes o que sente",
    "Confiança": "Desejo de incorporar em si",
    "Medo": "Desejo de se proteger",
    "Surpresa": "Suspensão dos desejos para se orientar",
    "Tristeza": "Desejo de reintegrar algo perdido",
    "Nojo": "Rejeição sobre algo",
    "Raiva": "Desejo de destruir",
    "Antecipação": "Desejo de explorar e examinar"
}

diades_db = {
    frozenset(["Alegria", "Confiança"]): "Amor",
    frozenset(["Alegria", "Medo"]): "Culpa",
    frozenset(["Alegria", "Surpresa"]): "Prazer",
    frozenset(["Alegria", "Tristeza"]): "Sentimentos Conflituosos",
    frozenset(["Alegria", "Nojo"]): "Morbidez",
    frozenset(["Alegria", "Raiva"]): "Orgulho",
    frozenset(["Alegria", "Antecipação"]): "Otimismo",
    frozenset(["Confiança", "Medo"]): "Submissão",
    frozenset(["Confiança", "Surpresa"]): "Curiosidade",
    frozenset(["Confiança", "Tristeza"]): "Sentimentalismo",
    frozenset(["Confiança", "Nojo"]): "Sentimentos Conflituosos",
    frozenset(["Confiança", "Raiva"]): "Dominação",
    frozenset(["Confiança", "Antecipação"]): "Esperança",
    frozenset(["Medo", "Surpresa"]): "Temor",
    frozenset(["Medo", "Tristeza"]): "Desespero",
    frozenset(["Medo", "Nojo"]): "Vergonha",
    frozenset(["Medo", "Raiva"]): "Conflito / Ódio contido",
    frozenset(["Medo", "Antecipação"]): "Ansiedade",
    frozenset(["Surpresa", "Tristeza"]): "Desaprovação",
    frozenset(["Surpresa", "Nojo"]): "Incredulidade",
    frozenset(["Surpresa", "Raiva"]): "Indignação",
    frozenset(["Surpresa", "Antecipação"]): "Confusão",
    frozenset(["Tristeza", "Nojo"]): "Remorso",
    frozenset(["Tristeza", "Raiva"]): "Inveja",
    frozenset(["Tristeza", "Antecipação"]): "Pessimismo",
    frozenset(["Nojo", "Raiva"]): "Desprezo",
    frozenset(["Nojo", "Antecipação"]): "Cinismo",
    frozenset(["Raiva", "Antecipação"]): "Agressividade"
}

# --- HEADER ---
st.title("🧩 Registro Emocional")
st.markdown("**Protótipo de Homologação** • Preencha passo a passo")
st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# BLOCO 1: GATILHO (SEMPRE VISÍVEL)
# ==============================================================================
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">1. Gatilho (O que aconteceu?)</div>', unsafe_allow_html=True)

situacao = st.text_area(
    "Descrição da Situação:", 
    label_visibility="collapsed",
    placeholder="Ex: Cheguei em casa e vi que as tarefas não foram feitas...",
    height=100,
    key="input_situacao"
)
st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# LÓGICA PROGRESSIVA: SÓ MOSTRA BLOCO 2 SE BLOCO 1 TIVER CONTEÚDO
# ==============================================================================
necessidade_descritiva = ""
necessidades_selecionadas = []
pensamento = ""
emocoes_selecionadas = []
acao = ""

if situacao: # Se o usuário digitou a situação...
    
    # --- BLOCO 2: NECESSIDADES ---
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">2. Necessidades</div>', unsafe_allow_html=True)

    st.markdown("**O que você desejava? Que necessidade acha que foi ferida em você, ou outro ou no ambiente?**")
    necessidade_descritiva = st.text_area(
        "Descrição da necessidade",
        label_visibility="collapsed",
        placeholder="Descreva seu desejo aqui...",
        height=80,
        key="input_nec_desc"
    )

    st.markdown("<br>**Classificação Técnica (Selecione até 3):**", unsafe_allow_html=True)
    necessidades_selecionadas = st.multiselect(
        "Selecione as categorias:",
        options=list(necessidades_db.keys()),
        max_selections=3,
        label_visibility="collapsed",
        key="input_nec_sel"
    )
    
    # Visualização das Necessidades
    if necessidades_selecionadas:
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        for nec in necessidades_selecionadas:
            central = necessidades_db.get(nec, "")
            st.markdown(f"""
            <div class="need-tag">
                <b>{nec}</b><br><small>↳ {central}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


    # ==============================================================================
    # LÓGICA PROGRESSIVA: SÓ MOSTRA BLOCO 3 SE BLOCO 2 TIVER CONTEÚDO
    # ==============================================================================
    if necessidade_descritiva: # Se descreveu a necessidade...

        # --- BLOCO 3: PROCESSAMENTO INTERNO ---
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">3. Processamento Interno</div>', unsafe_allow_html=True)

        # CAMPO 1: PENSAMENTO
        st.markdown("**O que você pensou?**")
        pensamento = st.text_area(
            "Campo de pensamento",
            label_visibility="collapsed",
            placeholder="O que passou pela sua cabeça?",
            height=100,
            key="input_pensamento"
        )

        # CAMPO 2: EMOÇÃO
        st.markdown("<br>**Qual sentimento sentiu? (Mix de Emoções)**", unsafe_allow_html=True)
        emocoes_selecionadas = st.multiselect(
            "Selecione até 2:",
            options=list(impulses_db.keys()),
            max_selections=2,
            label_visibility="collapsed",
            key="input_emocoes"
        )

        # Visualização e Cálculo de Díades
        if emocoes_selecionadas:
            st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
            cols_cards = st.columns(2) # Colunas corrigidas
            
            for idx, emo in enumerate(emocoes_selecionadas):
                impulso = impulses_db.get(emo, "")
                # Distribui os cards nas colunas disponíveis
                col_to_use = cols_cards[idx] if idx < 2 else cols_cards
                with col_to_use:
                    st.markdown(f"""
                    <div class="emotion-tag">
                        <b>{emo}</b><br><small>{impulso}</small>
                    </div>
                    """, unsafe_allow_html=True)

            if len(emocoes_selecionadas) == 2:
                chave = frozenset(emocoes_selecionadas)
                resultado = diades_db.get(chave, "Combinação Complexa")
                st.markdown(f"""
                <div class="result-box">
                    ⚡ Resultado: {resultado.upper()}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        
        # ==============================================================================
        # LÓGICA PROGRESSIVA: SÓ MOSTRA BLOCO 4 SE BLOCO 3 TIVER CONTEÚDO
        # ==============================================================================
        # Considera preenchido se tiver Pensamento OU Emoção
        if pensamento or emocoes_selecionadas: 

            # --- BLOCO 4: REAÇÃO COMPORTAMENTAL ---
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">4. Reação Comportamental</div>', unsafe_allow_html=True)

            st.markdown("**Como se comportou?**")
            acao = st.text_area(
                "Campo de ação", 
                label_visibility="collapsed",
                placeholder="Descreva sua ação ou fala...", 
                height=80,
                key="input_acao"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # --- BOTÃO FINAL ---
            if st.button("💾 Salvar Registro no Diário", use_container_width=True):
                st.balloons()
                
                registro = {
                    "situacao": situacao,
                    "necessidade_descritiva": necessidade_descritiva,
                    "necessidades_tecnicas": [
                        {"especifica": nec, "central": necessidades_db.get(nec)} 
                        for nec in necessidades_selecionadas
                    ],
                    "pensamento": pensamento,
                    "emocoes": emocoes_selecionadas,
                    "resultado_emocional": diades_db.get(frozenset(emocoes_selecionadas), "") if len(emocoes_selecionadas)==2 else None,
                    "acao": acao
                }
                
                st.success("Registro salvo com sucesso!")
                with st.expander("Ver JSON Gerado"):
                    st.json(registro)

    # Mensagens de orientação caso o usuário pare no meio do caminho
    elif not necessidade_descritiva:
        st.info("👆 Preencha a necessidade acima para continuar...")
    
elif not situacao:
    st.info("👆 Comece descrevendo o que aconteceu...")