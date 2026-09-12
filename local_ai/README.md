# Local AI Integration — PLACEHOLDER (Phase 3)

Per spec `03_Technical_Constraints_and_Local_AI.md`:

- **Ollama** at `http://localhost:11434` (local API only — never a cloud LLM)
- Suggested models (quantized, hardware-appropriate): phi3 / phi3.5,
  qwen2.5:3b or 7b, llama3.2:3b, gemma2:2b / 9b
- Uses: explain synthesis routes in Persian or English, suggest alternative
  strategies, answer contextual chemistry questions, interpret results
- Rules:
  - Connection is **optional** — سیلا must fully work when Ollama is not running
    (graceful degradation)
  - User chooses which model to use (`preferred_local_ai_model` already exists
    in `data/user_settings/settings.json`)
  - Responses coming from the local AI must be clearly labeled as such
- Models are stored locally under `data/models/` (or Ollama's own store);
  no automatic downloads — internet only on explicit user request
