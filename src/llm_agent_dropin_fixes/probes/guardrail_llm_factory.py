# guardrail_llm_factory.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7764
# Upstream repo: crewAIInc/crewAI #7764
# Category: other
# Root cause / claim: Factory that gives LLMGuardrail its own judge LLM, falling back to the agent's — your #7150 separation ask.
# Verifier note: Py wires a separate guardrail_llm; import path may need adjusting per version.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

from crewai.tools.guardrail import LLMGuardrail  # adjust import to your version

# Plug in your own judge model here (separate from the agent's LLM)
GUARDRAIL_LLM = None  # e.g. LLM(model="gpt-4o-mini", api_key=os.environ["..."])

def make_guardrail(description, agent_llm):
    """Use a dedicated judge LLM when set, else the agent's own (your #7150 ask)."""
    judge = GUARDRAIL_LLM or agent_llm
    return LLMGuardrail(description=description, llm=judge)

# guardrail = make_guardrail("output must be valid JSON", agent.llm)
if __name__ == "__main__":
    print("guardrail_llm factory ready")

