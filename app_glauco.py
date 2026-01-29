Abaixo, o código Python atualizado com o novo bloco de CSS injetado, aplicando esses conceitos:
import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Glauco App - UI Glassmorphism",
    page_icon="🧠",
    layout="centered"
)

# --- CSS MODERNO (Baseado nas Fontes: Glassmorfismo, Color-Mix, Animations) ---
st.markdown("""
    <style>
    /* 
       VARIÁVEIS DE DESIGN SYSTEM (Design Tokens) [16]
       Definimos as cores base para serem usadas com color-mix
    */
    :root {
        --primary-hue: 24;  /* Laranja base */
        --neutral-hue: 210; /* Cinza azulado */
        --glass-border: rgba(255, 255, 255, 0.2);
        --shadow-soft: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }

    /* 
       SUPORTE A LIGHT/DARK MODE NATIVO [9]
       O fundo se adapta à preferência do sistema.
    */
    .stApp {
        background: light-dark(#f8f9fa, #0e1117);
        font-family: 'Inter', sans-serif;
    }
    
    /* 
       GLASSMORFISMO [6] + ANIMAÇÃO DE ENTRADA [17]
       O card agora parece vidro fosco flutuando.
    */
    .glass-card {
        background: rgba(255, 255, 255, 0.65); /* Transparência para o vidro */
        backdrop-filter: blur(12px);          /* O desfoque [18] */
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: var(--shadow-soft);
        
        /* Animação suave de entrada */
        animation: slideUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        opacity: 0;
        transform: translateY(20px);
    }

    /* Dark mode adjustments para o card */
    @media (prefers-color-scheme: dark) {
        .glass-card {
            background: rgba(30, 30, 30, 0.60);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
    }

    @keyframes slideUp {
        to { opacity: 1; transform: translateY(0); }
    }

    /* 
       MICRO-INTERAÇÕES NOS CARDS DE SELEÇÃO [11]
       Efeito de 'lift' (levantar) e sombra ao passar o mouse.
    */
    .selection-card {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease; /* [19] */
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .selection-card:hover {
        transform: translateY(-2px) scale(1.01); /* Movimento sutil [13] */
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-color: rgba(0,0,0,0.05);
    }

    /* 
       USO DE COLOR-MIX() PARA GERAR TEMAS [8]
       Gera fundos suaves misturando a cor da emoção com branco/transparência
    */
    .tag-emotion {
        /* Mistura Laranja com 85% de branco (no light) ou preto (no dark) */
        background-color: color-mix(in srgb, orange, transparent 85%); 
        color: #d9480f;
        border-left: 4px solid #ffc078;
    }
    
    .tag-need {
        /* Mistura Cinza com 90% de transparência */
        background-color: color-mix(in srgb, slategray, transparent 90%);
        color: #495057;
        border-left: 4px solid #adb5bd;
    }

    /* Títulos Elegantes */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: light-dark(#2c3e50, #e0e0e0);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Resultado Final (Gradiente Suave) */
    .result-box {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.1), rgba(33, 150, 243, 0.2));
        border: 1px solid rgba(33, 150, 243, 0.3);
        color: #1976d2;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 15px;
        backdrop-filter: blur(4px);
    }
    </style>
""", unsafe_allow_html=True)

# --- DADOS (Mantidos da Fonte 17) ---
necessidades_db = {
    "Presença emocional consistente": "Necessidade central: sentir-se seguro, protegido e não abandonado",
    "Proteção física e emocional": "Necessidade central: sentir-se seguro, protegido e não abandonado",
    "Previsibilidade relacional": "Necessidade central: sentir-se seguro, protegido e não abandonado",
    "Responsividade às necessidades": "Necessidade central: sentir-se seguro, protegido e não abandonado",
    "Escuta genuína": "Necessidade central: ser visto e compreendido emocionalmente",
    "Reconhecimento dos sentimentos": "Necessidade central: ser visto e compreendido emocionalmente",
    "Aceitação das imperfeições": "Necessidade central: sentir-se digno de amor como se é",
    "Incentivo à independência": "Necessidade central: sentir-se capaz de agir por conta própria",
    "Feedback realista": "Necessidade central: sentir-se eficaz e capaz",
    "Limites psicológicos claros": "Necessidade central: desenvolver um 'eu' próprio",
    "Poder dizer 'não'": "Necessidade central: poder expressar o que sente e precisa",
    "Brincar / Humor": "Necessidade central: viver com leveza, jogo e vitalidade",
    "Regras claras": "Necessidade central: aprender limites seguros e consistentes",
    "Rotina / Estabilidade": "Necessidade central: sentir que o mundo é compreensível e confiável"
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
    frozenset(["Alegria", "Confiança"]): "Amor", frozenset(["Alegria", "Medo"]): "Culpa",
    frozenset(["Alegria", "Surpresa"]): "Prazer", frozenset(["Alegria", "Tristeza"]): "Sentimentos Conflituosos",
    frozenset(["Alegria", "Nojo"]): "Morbidez", frozenset(["Alegria", "Raiva"]): "Orgulho",
    frozenset(["Alegria", "Antecipação"]): "Otimismo", frozenset(["Confiança", "Medo"]): "Submissão",
    frozenset(["Confiança", "Surpresa"]): "Curiosidade", frozenset(["Confiança", "Tristeza"]): "Sentimentalismo",
    frozenset(["Confiança", "Nojo"]): "Sentimentos Conflituosos", frozenset(["Confiança", "Raiva"]): "Dominação",
    frozenset(["Confiança", "Antecipação"]): "Esperança", frozenset(["Medo", "Surpresa"]): "Temor",
    frozenset(["Medo", "Tristeza"]): "Desespero", frozenset(["Medo", "Nojo"]): "Vergonha",
    frozenset(["Medo", "Raiva"]): "Conflito / Ódio contido", frozenset(["Medo", "Antecipação"]): "Ansiedade",
    frozenset(["Surpresa", "Tristeza"]): "Desaprovação", frozenset(["Surpresa", "Nojo"]): "Incredulidade",
    frozenset(["Surpresa", "Raiva"]): "Indignação", frozenset(["Surpresa", "Antecipação"]): "Confusão",
    frozenset(["Tristeza", "Nojo"]): "Remorso", frozenset(["Tristeza", "Raiva"]): "Inveja",
    frozenset(["Tristeza", "Antecipação"]): "Pessimismo", frozenset(["Nojo", "Raiva"]): "Desprezo",
    frozenset(["Nojo", "Antecipação"]): "Cinismo", frozenset(["Raiva", "Antecipação"]): "Agressividade"
}

# --- HEADER ---
st.title("🧩 Diário Emocional")
st.markdown("Registro guiado baseado em TCC • **Design System v6**")
st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# BLOCO 1: GATILHO
# ==============================================================================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">📍 1. Gatilho (O que aconteceu?)</div>', unsafe_allow_html=True)

situacao = st.text_area(
    "Descrição da Situação:", 
    label_visibility="collapsed",
    placeholder="Ex: Cheguei em casa e vi que as tarefas não foram feitas...",
    height=100,
    key="input_sit"
)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica de Progressão (Só mostra o próximo se o anterior estiver preenchido)
necessidade_descritiva = ""
necessidades_selecionadas = []
pensamento = ""
emocoes_selecionadas = []
acao = ""

if situacao:
    # --- BLOCO 2: NECESSIDADES ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">❤️ 2. Necessidades</div>', unsafe_allow_html=True)

    st.markdown("**O que você desejava? Que necessidade acha que foi ferida?**")
    necessidade_descritiva = st.text_area(
        "desc_nec", label_visibility="collapsed",
        placeholder="Descreva seu desejo aqui...", height=80
    )

    st.markdown("<br>**Classificação Técnica:**", unsafe_allow_html=True)
    necessidades_selecionadas = st.multiselect(
        "Selecione as categorias:",
        options=list(necessidades_db.keys()),
        max_selections=3,
        label_visibility="collapsed"
    )

    if necessidades_selecionadas:
        st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
        for nec in necessidades_selecionadas:
            central = necessidades_db.get(nec, "")
            # Aplica a classe de micro-interação 'selection-card' e cor dinâmica 'tag-need'
            st.markdown(f"""
            <div class="selection-card tag-need">
                <b>{nec}</b><br><small style="opacity:0.8">{central}</small>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if necessidade_descritiva:
        # --- BLOCO 3: PROCESSAMENTO INTERNO ---
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">🧠 3. Processamento Interno</div>', unsafe_allow_html=True)

        st.markdown("**O que você pensou?**")
        pensamento = st.text_area(
            "pensamento", label_visibility="collapsed",
            placeholder="O que passou pela sua cabeça?", height=100
        )

        st.markdown("<br>**Qual sentimento sentiu? (Mix de Emoções)**", unsafe_allow_html=True)
        emocoes_selecionadas = st.multiselect(
            "emo_sel", options=list(impulses_db.keys()),
            max_selections=2, label_visibility="collapsed"
        )

        if emocoes_selecionadas:
            st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
            cols_cards = st.columns(2)
            for idx, emo in enumerate(emocoes_selecionadas):
                impulso = impulses_db.get(emo, "")
                col_use = cols_cards[idx] if idx < 2 else cols_cards
                with col_use:
                    # Aplica cor dinâmica 'tag-emotion'
                    st.markdown(f"""
                    <div class="selection-card tag-emotion">
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

        if pensamento or emocoes_selecionadas:
            # --- BLOCO 4: COMPORTAMENTO ---
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-header">🏃 4. Reação Comportamental</div>', unsafe_allow_html=True)

            st.markdown("**Como se comportou?**")
            acao = st.text_area(
                "acao", label_visibility="collapsed",
                placeholder="Descreva sua ação ou fala...", height=80
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Botão Final
            if st.button("💾 Salvar Registro no Diário", use_container_width=True):
                st.balloons()
                st.success("Registro salvo com sucesso!")
                # JSON Simulado
                registro = {
                    "situacao": situacao,
                    "necessidade": necessidade_descritiva,
                    "tags_necessidade": necessidades_selecionadas,
                    "pensamento": pensamento,
                    "emocoes": emocoes_selecionadas,
                    "acao": acao
                }
                with st.expander("Ver JSON"):
                    st.json(registro)
    
    elif not necessidade_descritiva:
        st.info("👆 Continue preenchendo as necessidades para prosseguir...")
elif not situacao:
    st.info("👆 Comece descrevendo o gatilho acima...")
