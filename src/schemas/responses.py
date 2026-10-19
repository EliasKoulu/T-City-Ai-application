from pydantic import BaseModel, Field

from typing import Optional


class AIResponse(BaseModel):
    """
    Standardisoitu vastausmalli tekoälypalvelun (AIService) palauttamille vastauksille.
    """
    content: str = Field(description="Tekoälyn tuottama vastausteksti tai virheilmoitus käyttäjälle.")
    success: bool = Field(default=True, description="Ilmoittaa, onnistuiko pyyntö vai tuliko virhe.")
    error_message: Optional[str] = Field(default=None, description="Tarkempi tekninen virheilmoitus, jos success on False.")


class PropertyComparison(BaseModel):
    property_a_name: str = Field(description="Ensimmäisen asunnon nimi tai osoite")
    property_b_name: str = Field(description="Toisen asunnon nimi tai osoite")
    price_comparison: str = Field(description="Pyyntihintojen ja neliöhintojen vertailu")
    size_and_rooms: str = Field(description="Pinta-alan ja huoneluvun vertailu")
    maintenance_fee: str = Field(description="Vastikkeiden vertailu")
    condition_and_renovations: str = Field(description="Asuntojen kunto ja tehdyt/tulevat remontit (esim. putkiremontti)")
    pros_cons_summary: str = Field(description="Molemman asunnon hyvät ja huonot puolet")
    verdict: str = Field(description="Yhteenveto ja suositus siitä, kummalle ostajalle kumpikin asunto sopii")