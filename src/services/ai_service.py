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
1. Käytä AINOASTAAN annettuja tiedostoja lähteenä. Älä keksi omia hintoja, neliöitä, hoitovastikkeita tai remonttitietoja.
2. Kopioi ja täytä AINA alla oleva kiinteä Markdown-taulukko. Älä poista rivejä tai muuta vasemman sarakkeen ominaisuuksia. Etsi teksteistä otsikoita vastaavat tiedot Asunto A ja Asunto B -sarakkeisiin. Jos jotain tietoa ei löydy, kirjoita sen solun kohdalle pelkkä "-":

| Ominaisuus | Asunto A | Asunto B |
| :--- | :--- | :--- |
| Hinta | | |
| Pinta-ala | | |
| Huoneiston kokoonpano | | |
| Rakennusvuosi ja tyyppi | | |
| Tontin omistus | | |
| Hoitovastike | | |
| Kunto | | |
| Lämmitysmuoto | | |

3. Esitä taulukon alapuolella MAKSIMISSAAN 4 lauseen mittainen yhteenveto, jossa kerrotaan lyhyesti mahdolliset merkittävät erot.
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
        self.rag_service = None 

    def _get_client(self) -> OllamaModelClient:
        if self.model_client is None:
            self.model_client = OllamaModelClient()
        return self.model_client
        
    def _get_rag(self) -> RAGService:
        if self.rag_service is None:
            self.rag_service = RAGService()
        return self.rag_service

    def process_message(self, pdf1_path: str, pdf2_path: str, user_query: str) -> AIResponse:
    
        if not pdf1_path or not pdf2_path:
            return AIResponse(
                content="⚠️ Lataa molemmat asuntoesitteet (PDF) ennen vertailua.",
                success=False,
                error_message="Missing PDF files.",
            )

        try:
            
            rag = self._get_rag()
            rag.process_documents(pdf1_path, pdf2_path)

            vakio_hakusanat = "Velaton hinta Myyntihinta Hoitovastike Yhtiövastike Asuinpinta-ala Huoneiston kokoonpano Rakennusvuosi Tontin omistus Kunto Lämmitysmuoto"
            
            if user_query and user_query.strip():

                hakusana = f"{user_query} {vakio_hakusanat}"
                erityistoive = user_query.strip()
            else:

                hakusana = vakio_hakusanat
                erityistoive = "Täytä vertailutaulukko tarkasti annettujen lähdetietojen perusteella."
            

            context = rag.search_context(hakusana, top_k=8)
            
            user_prompt = f"""Käyttäjän erityistoive vertailulle: "{erityistoive}"

LÄHDETEKSTI (Oikotien esitteistä irrotettu tieto):
{context}

Käytä käyttäjän erityistoivetta ja yllä olevaa lähdetekstiä niin, että vastaat TÄYSIN käyttäjän kyselyyn.

Taulukon sekä yhteenvedon alle oma osuus, jonka otsikko on: "  Käyttäjän kysymys: {user_query}". Vastaa käyttäjän kysymykseen lyhyesti ja ytimekkäästi, mutta vain annettujen tietojen perusteella. Älä keksi mitään tietoja itse. Jos kysymykseen ei löydy vastausta, kerro se selkeästi.
"""


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

def generate_response(pdf1_path: str, pdf2_path: str, user_query: str, service: Optional[AIService] = None) -> str:
    """
    Main reusable service entry point used by the UI layer.
    """
    active_service = service or AIService()
    response = active_service.process_message(pdf1_path, pdf2_path, user_query)
    return response.content