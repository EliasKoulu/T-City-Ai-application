from unittest.mock import MagicMock, patch
import pytest
 
from src.config import config
from src.models.model_client import (
    OllamaConnectionError,
    ModelNotFoundError,
)
from src.services.ai_service import AIService, generate_response
 
 
def test_config_loading():
    """Varmistaa, että asetukset latautuvat oikein."""
    assert config.ollama_base_url is not None
    assert config.model_name is not None
    assert isinstance(config.ollama_base_url, str)
    assert isinstance(config.model_name, str)
 
 
def test_missing_pdf_inputs_validation():
    """Varmistaa, että puuttuvat PDF-tiedostot estävät haun ilman mallin kutsumista."""
    mock_client = MagicMock()
    service = AIService(model_client=mock_client)
 
    # Testataan tilannetta, jossa PDF-polut puuttuvat
    response = service.process_message("", "", "Vertaile hintoja")
    assert response.success is False
    assert "Lataa molemmat asuntoesitteet" in response.content
    assert mock_client.generate.call_count == 0
 
 
@patch("src.services.ai_service.AIService._get_rag")
def test_successful_response_generation(mock_get_rag):
    """Varmistaa, että kelvolliset syötteet kutsuvat mallia ja palauttavat vastauksen."""
    # Ohitetaan RAG-palvelu valeelementillä (mock), jotta testi on salamannopea
    mock_rag = MagicMock()
    mock_rag.search_context.return_value = "LÄHDETIEDOT: Valekonteksti asunnoista"
    mock_get_rag.return_value = mock_rag
 
    mock_client = MagicMock()
    mock_client.generate.return_value = "| Ominaisuus | Asunto 1 | Asunto 2 |\n| Hinta | 100k | 200k |"
    service = AIService(model_client=mock_client)
 
    result_text = generate_response("asunto1.pdf", "asunto2.pdf", "Vertaile hintoja", service=service)
 
    assert "| Ominaisuus | Asunto 1 | Asunto 2 |" in result_text
    mock_client.generate.assert_called_once()
 
 
def test_ollama_connection_error_handling():
    """Varmistaa, että Ollamas-yhteysvirhe käsitellään siististi käyttäjälle."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = OllamaConnectionError("Connection refused")
    service = AIService(model_client=mock_client)
    service.rag_service = MagicMock()  # Ohitetaan RAG
 
    response = service.process_message("asunto1.pdf", "asunto2.pdf", "Vertaile")
 
    assert response.success is False
    assert "Could not connect to Ollama" in response.content
 
 
def test_model_not_found_error_handling():
    """Varmistaa, että puuttuvan mallin virhe käsitellään siististi."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = ModelNotFoundError("Model qwen3:8b not found")
    service = AIService(model_client=mock_client)
    service.rag_service = MagicMock()  # Ohitetaan RAG
 
    response = service.process_message("asunto1.pdf", "asunto2.pdf", "Vertaile")
 
    assert response.success is False
    assert "unavailable" in response.content