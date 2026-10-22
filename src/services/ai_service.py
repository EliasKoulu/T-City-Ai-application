# from typing import Optional
# from src.models.model_client import (
#     OllamaModelClient,
#     ModelClientError,
#     OllamaConnectionError,
#     ModelNotFoundError,
# )
# from src.schemas.responses import UserRequest, AIResponse


# class AIService:
#     """
#     Application service layer responsible for validating user input,
#     orchestrating model client requests, and catching exceptions gracefully.
#     """

#     def __init__(self, model_client: Optional[OllamaModelClient] = None):
#         # Allow injecting custom/mock model_client for simple testing
#         self.model_client = model_client

#     def _get_client(self) -> OllamaModelClient:
#         """Returns active model client, initializing default client if none provided."""
#         if self.model_client is None:
#             self.model_client = OllamaModelClient()
#         return self.model_client

#     def process_message(self, user_message: str) -> AIResponse:
#         """
#         Processes a raw user message string and returns a structured AIResponse.
#         Catches technical failures and converts them to friendly user-facing messages.
#         """
#         # 1. Validate empty input
#         if not user_message or not user_message.strip():
#             return AIResponse(
#                 content="Please enter a message before sending.",
#                 success=False,
#                 error_message="User message was empty.",
#             )

#         try:
#             # 2. Schema validation
#             request = UserRequest(message=user_message.strip())

#             # 3. Call model client
#             client = self._get_client()
#             response_text = client.generate(request.message)

#             return AIResponse(
#                 content=response_text,
#                 success=True,
#             )

#         except OllamaConnectionError as err:
#             return AIResponse(
#                 content=(
#                     "[Error] Could not connect to Ollama.\n\n"
#                     "Please verify that Ollama is installed and running locally on your machine."
#                 ),
#                 success=False,
#                 error_message=str(err),
#             )

#         except ModelNotFoundError as err:
#             return AIResponse(
#                 content=(
#                     f"[Error] The configured AI model is unavailable in Ollama.\n\n"
#                     f"Please verify your MODEL_NAME setting or run 'ollama run <model_name>'."
#                 ),
#                 success=False,
#                 error_message=str(err),
#             )

#         except ModelClientError as err:
#             return AIResponse(
#                 content="[Error] An unexpected communication error occurred with the AI model.",
#                 success=False,
#                 error_message=str(err),
#             )

#         except Exception as err:
#             return AIResponse(
#                 content="[Error] An unexpected application error occurred.",
#                 success=False,
#                 error_message=str(err),
#             )


# def generate_response(user_message: str, service: Optional[AIService] = None) -> str:
#     """
#     Main reusable service entry point used by the UI layer.
    
#     Accepts user input message, passes it to the AI service, and returns
#     the generated text response (or a friendly error message).
#     """
#     active_service = service or AIService()
#     response = active_service.process_message(user_message)
#     return response.content

from typing import Optional
from src.models.model_client import (
    OllamaModelClient,
    ModelClientError,
    OllamaConnectionError,
    ModelNotFoundError,
)
from src.schemas.responses import AIResponse

# Tuodaan Arin tekemä RAG-palvelu
from src.capabilities.rag import RAGService

#Määritellään tekoälyn rooli ja toimintasäännöt
SYSTEM_PROMPT = """Olet ammattimainen ja objektiivinen kiinteistöalan asiantuntija. Tehtäväsi on vertailla kahta Oikotien asuntoilmoitusta täsmällisesti.

Noudata tiukasti seuraavia sääntöjä:
1. Käytä AINOASTAAN annettuja tiedostoja lähteenä. Älä keksi omia hintoja, neliöitä, hoitovastikkeita tai remonttitietoja. Mikäli tietoa ei löydy toisesta esitteestä, kirjoita taulukkoon " Ei ilmoitettu. ".
2. Rakenna vertailusta aina selkeä Markdown-taulukko (sarakkeet: Ominaisuus | Asunto A | Asunto B).
3. Esitä taulukon alapuolella lyhyt yhteenveto asuntojen suurimmista eroista sekä ostajasuositus.
4. Vertailtavien tiedostojen otsikko on vasemmalla ja itse otsikkoa vastaava tieto oikealla. Tämä osuus tulee tiedostoissa olevan tekstin jälkeen.
5. Tiedoistoissa on taulukko jossa vasemmassa sarakkeessa on ominaisuuden nimi ja oikealla sarakkeessa sen arvo. Käytä näitä tietoja vertailussa.
"""




class AIService:
    """
    Application service layer responsible for validating user input,
    orchestrating model client requests, and catching exceptions gracefully.
    """

    def __init__(self, model_client: Optional[OllamaModelClient] = None):
        self.model_client = model_client
        self.rag_service = None # Alustetaan RAG vain tarvittaessa

    def _get_client(self) -> OllamaModelClient:
        if self.model_client is None:
            self.model_client = OllamaModelClient()
        return self.model_client
        
    def _get_rag(self) -> RAGService:
        if self.rag_service is None:
            self.rag_service = RAGService()
        return self.rag_service

    def process_message(self, pdf1_path: str, pdf2_path: str, user_query: str) -> AIResponse:
        """
        Käsittelee käyttöliittymästä tulevat PDF-tiedostot ja käyttäjän syötteen.
        Käyttää RAG-putkea tiedonhakuun ja generoi vertailun tekoälymallilla.
        """
        # 1. Validointi: Varmistetaan, että molemmat tiedostot on ladattu
        if not pdf1_path or not pdf2_path:
            return AIResponse(
                content="⚠️ Lataa molemmat asuntoesitteet (PDF) ennen vertailua.",
                success=False,
                error_message="Missing PDF files.",
            )

        try:
            # 2. RAG-käsittely: Luetaan ja vektoroidaan asuntodokumentit
            rag = self._get_rag()
            rag.process_documents(pdf1_path, pdf2_path)
            
            # 3. Tiedonhaku: Etsitään oleellinen konteksti vektoritietokannasta
            # Jos käyttäjä ei antanut erityistoivetta, käytetään yleistä vertailuhakua
            hakusana = user_query if user_query and user_query.strip() else "asuntojen koko, hinta, kunto ja lämmitys"
            context = rag.search_context(hakusana, top_k=6)
            
            erityistoive = user_query if user_query and user_query.strip() else "Tee yleinen vertailu tärkeimmistä ominaisuuksista."
            
            user_prompt = f"""Käyttäjän erityistoive vertailulle: "{erityistoive}"

LÄHDETEKSTI (Oikotien esitteistä irrotettu tieto):
{context}

Rakenna näiden tietojen pohjalta selkeä vertailu.
"""

            # 5. Kutsutaan Ollama-mallia
            client = self._get_client()
            response_text = client.generate(
                prompt=user_prompt,
                system_prompt=SYSTEM_PROMPT,
                temperature=0.1
            )

            return AIResponse(
                content=response_text,
                success=True,
            )

        # Opettajan alkuperäiset virheenhallinnat säilytettyinä
        except OllamaConnectionError as err:
            return AIResponse(
                content="[Error] Could not connect to Ollama. Please verify that Ollama is running.",
                success=False,
                error_message=str(err),
            )
        except ModelNotFoundError as err:
            return AIResponse(
                content=f"[Error] The configured AI model is unavailable in Ollama. Verify your MODEL_NAME setting.",
                success=False,
                error_message=str(err),
            )
        except ModelClientError as err:
            return AIResponse(
                content="[Error] An unexpected communication error occurred with the AI model.",
                success=False,
                error_message=str(err),
            )
        except Exception as err:
            return AIResponse(
                content=f"[Error] An unexpected application error occurred: {str(err)}",
                success=False,
                error_message=str(err),
            )


# Päivitetty entry point UI-kerrokselle
def generate_response(pdf1_path: str, pdf2_path: str, user_query: str, service: Optional[AIService] = None) -> str:
    """
    Main reusable service entry point used by the UI layer.
    """
    active_service = service or AIService()
    response = active_service.process_message(pdf1_path, pdf2_path, user_query)
    return response.content
