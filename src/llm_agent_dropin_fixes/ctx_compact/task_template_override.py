# task_template_override.py
# Source issue: https://github.com/crewAIInc/crewAI/issues/7766
# Upstream repo: crewAIInc/crewAI #7766
# Category: ctx_compact
# Root cause / claim: Targeted shim that swaps the hard-coded 'you MUST return...' line for the softer wording the MAST study argues for.
# Verifier note: Py installs the override; real fix belongs in core, but it proves the softer line locally.
# Plug in your own client/model — no hardcoded keys. Drop-in reference fix.

ORIGINAL = "you MUST return the actual complete content as the final answer, not a summary."
SOFTER = ("Return the complete content as the final answer, or state clearly "
          "what information is missing.")

import crewai.task as _task

def install_soft_line():
    base = _task.Task.__init__
    def new_init(self, *args, **kwargs):
        base(self, *args, **kwargs)
        if isinstance(getattr(self, "description", ""), str):
            self.description = self.description.replace(ORIGINAL, SOFTER)
    _task.Task.__init__ = new_init

# Call install_soft_line() once at import time, before building Tasks.
if __name__ == "__main__":
    install_soft_line()
    print("softened task line installed")

