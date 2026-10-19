from src.services.ai_service import AIService

# PDF-tiedostojen polut
pdf1 = "data/oikotie-24735837-purpurikuja-7-21330-turku.pdf"
pdf2 = "data/oikotie-24741542-tammelininkatu-3-20380-turku.pdf"

print("Ajetaan tekoälyvertailua...")

service = AIService()
response = service.process_message(
    pdf1_path=pdf1,
    pdf2_path=pdf2,
    user_query="Kumpi asunto sopii paremmin lapsiperheelle?"
)

print("\n--- TEKOÄLYN VASTAUS ---")
print("Onnistui:", response.success)
print("Sisältö:\n", response.content)
print("\nTarkka virheviesti:", response.error_message)