from pydantic import BaseModel, Field


class PropertyComparison(BaseModel):
    property_a_name: str = Field(description="Ensimmäisen asunnon nimi tai osoite")
    property_b_name: str = Field(description="Toisen asunnon nimi tai osoite")
    price_comparison: str = Field(description="Pyyntihintojen ja neliöhintojen vertailu")
    size_and_rooms: str = Field(description="Pinta-alan ja huoneluvun vertailu")
    condition_and_renovations: str = Field(description="Asuntojen kunto ja tehdyt/tulevat remontit (esim. putkiremontti)")
    pros_cons_summary: str = Field(description="Molemman asunnon hyvät ja huonot puolet")
    verdict: str = Field(description="Yhteenveto ja suositus siitä, kummalle ostajalle kumpikin asunto sopii")