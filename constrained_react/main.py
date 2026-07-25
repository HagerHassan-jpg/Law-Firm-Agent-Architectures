from agent import run_agent

if __name__ == "__main__":
    test_ids = ["CASE-001", "CASE-002", "CASE-003", "CASE-004"]

    for case_id in test_ids:
        print(f"\n--- {case_id} ---")
        result = run_agent(case_id)
        print(result)
