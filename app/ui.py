import gradio as gr
from src.services.ai_service import generate_response

custom_css = """
/* Otsikot mustiksi */
label span {
    color: black !important;
}
/* Tekstikentän teksti mustaksi */
textarea, input {
    color: black !important;
}
/* Ladatun tiedoston (tumma laatikko) tiedostonimi ja koko valkoiseksi */
.file-preview-holder span, 
.file-preview-holder a,
.file-preview span,
.file-preview a {
    color: white !important; 
}
"""

custom_theme = gr.themes.Soft(
    primary_hue="emerald",
    neutral_hue="slate",
).set(
    body_background_fill="white",
    body_background_fill_dark="white",
    body_text_color="black",
    body_text_color_dark="black",
    
    block_background_fill="#f8fafc",
    block_background_fill_dark="#f8fafc",
    block_border_width="2px",
    block_border_color="#86efac",
    block_border_color_dark="#86efac",
    
    block_label_background_fill="#dcfce7", 
    block_label_background_fill_dark="#dcfce7",
    block_label_text_color="black",
    block_label_text_color_dark="black",
    
    input_background_fill="white",
    input_background_fill_dark="white",
    input_border_width="2px",
    input_border_color="#86efac",
    input_border_color_dark="#86efac",
    input_placeholder_color="#94a3b8",
    input_placeholder_color_dark="#94a3b8",
    
    button_primary_background_fill="#86efac",
    button_primary_background_fill_dark="#86efac",
    button_primary_background_fill_hover="#4ade80",
    button_primary_text_color="black",
    button_primary_text_color_dark="black",
)

def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Oikotie-vertailukone", theme=custom_theme, css=custom_css) as demo:
        gr.Markdown(
            """
            # 🏠 Oikotie Asuntoesitteiden Vertailukone
            
            Tervetuloa asuntotyökaluun! Lataa alle kaksi PDF-muotoista asuntoesitettä Oikotiestä. 
            Tekoäly lukee esitteet ja tekee niistä sinulle tiivistetyn vertailun.
            """
        )

        with gr.Row():
            with gr.Column():
                pdf1_input = gr.File(
                    label="Lataa Asunto 1:n esite (PDF)", 
                    file_types=[".pdf"],
                    type="filepath" 
                )
            with gr.Column():
                pdf2_input = gr.File(
                    label="Lataa Asunto 2:n esite (PDF)", 
                    file_types=[".pdf"],
                    type="filepath"
                )

        with gr.Row():
            user_query = gr.Textbox(
                lines=2,
                placeholder="Esim. Vertaile näiden asuntojen putkiremonttitilannetta ja lämmitysmuotoja...",
                label="Mitä haluat erityisesti vertailla? (Valinnainen)"
            )

        submit_btn = gr.Button("Vertaile asunnot", variant="primary")

        with gr.Row():
            output_box = gr.Markdown(
                label="Vertailun tulos"
            )

        def show_loading():
            return "⏳ **Tekoäly lukee esitteitä ja rakentaa vertailua, odota hetki...** *(Ensimmäisellä kerralla mallin lataus muistiin voi kestää tovin)*"

        submit_btn.click(
            fn=show_loading,
            inputs=None,
            outputs=output_box,
            queue=False
        ).then(
            fn=generate_response,
            inputs=[pdf1_input, pdf2_input, user_query],
            outputs=output_box,
        )
        
        user_query.submit(
            fn=show_loading,
            inputs=None,
            outputs=output_box,
            queue=False
        ).then(
            fn=generate_response,
            inputs=[pdf1_input, pdf2_input, user_query],
            outputs=output_box,
        )

    return demo