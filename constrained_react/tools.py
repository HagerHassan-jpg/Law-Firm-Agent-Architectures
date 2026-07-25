from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parent.parent))  # noqa: E402

# allow importing from shared/

from shared.tools import (
    load_case,
    evaluate_documents,
    evaluate_conflict,
    evaluate_specialist,
    evaluate_client_history,
)


# ==== TOOL ALLOW-LIST (schema-validated tools only) ====
ALLOWED_TOOLS = {
    "evaluate_documents": evaluate_documents,
    "evaluate_conflict": evaluate_conflict,
    "evaluate_specialist": evaluate_specialist,
    "evaluate_client_history": evaluate_client_history,
}
