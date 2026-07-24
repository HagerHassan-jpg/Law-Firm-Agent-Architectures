import json
from shared.tools import load_case
from agent import run_agent


def main():
    print("=" * 60)
    print("Law Firm Case Intake Evaluation")
    print("Unconstrained ReAct Agent")
    print("=" * 60)

    case_id = input("\nEnter Case ID: ").strip()

    try:
        case = load_case(case_id)
    except Exception as e:
        print(f"\nError loading case: {e}")
        return

    if case is None:
        print(f"\nCase '{case_id}' not found.")
        return

    print(f"\nEvaluating Case: {case['case_id']}...\n")

    try:
        result = run_agent(case)

        print("=" * 60)
        print("Evaluation Result")
        print("=" * 60)
        print(json.dumps(result, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"\nError during evaluation: {e}")


if __name__ == "__main__":
    main()
