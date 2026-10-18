import gradio as gr
from src.services.ai_service import generate_response

def build_ui() -> gr.Blocks:
    """
    Constructs the Gradio web interface.
    
    Architectural Principle: The UI communicates strictly with `generate_response()`
    in the AI service layer and never directly with Ollama or the model client.
    """
    with gr.Blocks(title="Oikotie-vertailukone", theme=gr.themes.Soft()) as demo:
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
                    type="filepath" # Palauttaa tiedostopolun suoraan palvelukerrokselle
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
            # Markdown-komponentti renderöi tekoälyn tekemät taulukot kauniisti
            output_box = gr.Markdown(
                label="Vertailun tulos"
            )

        # Connect UI actions exclusively to the service layer function
        submit_btn.click(
            fn=generate_response,
            inputs=[pdf1_input, pdf2_input, user_query],
            outputs=output_box,
        )
        user_query.submit(
            fn=generate_response,
            inputs=[pdf1_input, pdf2_input, user_query],
            outputs=output_box,
        )

    return demo