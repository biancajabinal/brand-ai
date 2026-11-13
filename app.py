import streamlit as st
import google.generativeai as genai

# Configuração da página otimizada para visualização em Tablet/Mobile
st.set_page_config(
    page_title="Brand Health & AI Audit", 
    page_icon="🛡️", 
    layout="wide"
)

# Estilização visual com paleta sofisticada (tons neutros e elegantes)
st.markdown("""
    <style>
    .main { background-color: #F9F6F0; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #1A1A1A; }
    .card { background-color: #FFFFFF; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.04); margin-bottom: 20px; }
    .stButton>button { background-color: #1A1A1A; color: #FFFFFF; border-radius: 8px; width: 100%; font-weight: 600; padding: 10px; }
    .stButton>button:hover { background-color: #333333; color: #FFF; }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho do Painel
st.title("🛡️ Brand Health & AI Audit")
st.markdown("**Sistema de Monitoramento e Construção de Posicionamento de Marca**")
st.markdown("---")

# Barra Lateral (Menu de Configuração para a Consultoria)
st.sidebar.header("⚙️ Painel de Controle")
api_key_input = st.sidebar.text_input("Insira sua Chave API do Gemini", type="password")
st.sidebar.markdown("---")
cliente_nome = st.sidebar.text_input("Nome da Marca em Análise", "Ex: Aura Ateliê")

st.sidebar.markdown("### 📥 Insumos da Marca")
manual_input = st.sidebar.text_area("Cole o Manual de Identidade (Propósito, Tom, Cores)", 
    "Ex: Propósito: Vestir com elegância atemporal.\nTom: Sofisticado, inspirador.\nPaleta: Preto, Off-white, Terracota.")
dados_recentes = st.sidebar.text_area("Cole os dados recentes (Posts, Comentários, Menções)", 
    "Ex: Post com carrossel neutro elogiado, mas comentário apontando dúvida sobre versatilidade.")

st.sidebar.markdown("---")
rodar_auditoria = st.sidebar.button("✨ Executar Auditoria de Branding")

# Área Principal do Dashboard
if rodar_auditoria:
    if not api_key_input:
        st.error("Por favor, insira a sua Chave API do Gemini na barra lateral para ativar a inteligência.")
    elif not manual_input or not dados_recentes:
        st.warning("Preencha o Manual de Identidade e os dados recentes na barra lateral para gerar a análise.")
    else:
        # Configurando a API do Gemini com o Prompt Mestre da Diretora de Branding
        genai.configure(api_key=api_key_input)
        
        system_prompt = """
        Você é uma Diretora de Branding Sênior e Estrategista de Marcas de elite, especialista em gestão de identidade, construção de valor de marca e alinhamento de posicionamento para empresas em expansão. 
        Sua missão é atuar como a inteligência analítica de um painel de saúde de marca, ajudando a fundadora a acompanhar a construção contínua da sua marca e garantir que a empresa esteja transmitindo exatamente a imagem desejada para o seu público-alvo.
        Mantenha um tom assertivo, elegante, estratégico e inspirador, falando com a autoridade de quem domina a percepção de mercado.
        Estrutura obrigatória da resposta (seja concisa e executiva):
        1. AUDITORIA VISUAL: Avalie a fidelidade estética ao manual, aponte o nível de consistência visual e destaque se a direção de arte está reforçando a imagem desejada.
        2. SAÚDE EMOCIONAL & PERCEPÇÃO: Analise o termômetro de sentimento e o comportamento do público. O que eles estão captando da marca está alinhado com a essência e o público-alvo pretendido, ou há ruídos?
        3. DIRETRIZES DA DIRETORA: Entregue de 2 a 3 ações práticas e imediatas para ajustar a comunicação, estreitar o laço com o público-alvo e fortalecer a construção da marca.
        """
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=system_prompt
        )
        
        prompt_usuario = f"""
        Analise a marca '{cliente_nome}' com base nos seguintes dados:
        
        MANUAL DE IDENTIDADE:
        {manual_input}
        
        DADOS RECENTES:
        {dados_recentes}
        """
        
        with st.spinner("A Diretora de Branding está analisando os dados e estruturando o painel..."):
            try:
                response = model.generate_content(prompt_usuario)
                
                # Exibindo os resultados de forma limpa na tela principal
                st.success(f"Análise concluída com sucesso para: **{cliente_nome}**")
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a API: {e}")
else:
    # Tela inicial antes de rodar
    st.info("👈 Preencha os dados da marca na barra lateral à esquerda e clique em **'Executar Auditoria de Branding'** para gerar o painel estratégico.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 O que este painel avalia:")
        st.markdown("- **Fidelidade Estética:** Alinhamento do visual com o manual.")
        st.markdown("- **Saúde Emocional:** O que o público realmente está captando.")
        st.markdown("- **Diretrizes Estratégicas:** Ações práticas da Diretora.")
    with col2:
        st.markdown("### 📱 Perfeito para o Tablet")
        st.markdown("Toda a interface foi desenhada para rodar direto no navegador, permitindo que você apresente o diagnóstico com elegância para suas clientes.")
