# CLA / سیلا - Technical Constraints & Local AI Integration

## Hardware Constraints (Very Important)

The target system has limited resources:

- CPU: Intel Core i5-4300M (Haswell, old generation)
- RAM: 16 GB
- GPU: NVIDIA GT 730M (very weak, ~1 GB VRAM) + Intel HD Graphics
- Storage: 512 GB SSD

### Consequences
- Large language models (13B+) will be extremely slow or impossible to run comfortably.
- Prefer quantized small-to-medium models (3B – 8B parameters).
- Chemistry calculations (RDKit, AiZynthFinder) are acceptable but can become slow on complex molecules.
- Always give the user control over computation time and search depth.

## Local AI Integration Strategy

### Recommended Tool
**Ollama** (easiest and most practical for this hardware)

### Suggested Models to Support (in order of preference)
1. phi3 or phi3.5 (Microsoft) – good reasoning for size
2. qwen2.5:3b or qwen2.5:7b
3. llama3.2:3b
4. gemma2:2b or gemma2:9b (if it fits)

### How Local AI Should Be Used
- Explain synthesis routes in natural language (Persian or English)
- Suggest alternative strategies
- Answer contextual chemistry questions
- Help interpret results
- Optional: assist in molecule design reasoning

### Implementation Notes
- Connect via Ollama’s local API (http://localhost:11434)
- Make the connection optional (system must work even if no local AI is running)
- Allow user to choose which model to use
- Clearly indicate when the response is coming from the local AI

## Offline-First Rules

- No automatic internet requests.
- All models, stocks, and databases must be stored locally.
- Internet access only when the user explicitly clicks an “Update from Internet” button.
- Cache any downloaded information locally for future offline use.

## Performance Philosophy

- Quality of chemical reasoning and results is more important than speed.
- Provide user controls such as:
  - Maximum search time
  - Search depth / number of iterations
  - Number of routes to generate
- Show progress indicators during long computations.

## Recommended Development Approach for Weak Hardware

1. Start with lightweight UI (Streamlit is acceptable for early versions).
2. Optimize AiZynthFinder settings for lower resource usage.
3. Use quantized models only.
4. Avoid heavy frontend frameworks in the first versions if they cause performance issues.
5. Make every heavy computation cancellable by the user.

## Notes for Coding AI
- Always design with the limited hardware in mind.
- Never assume powerful GPU or high RAM.
- Provide graceful degradation (system should still work if local AI is not available).
- Give the user clear feedback about expected processing time.
