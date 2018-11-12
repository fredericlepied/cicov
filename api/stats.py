def get_rfes_stats(tests, test_results):
    count = len(tests)
    success = 0
    tests_ids = [t["id"] for t in tests]
    for test_result in test_results:
        if test_result["test"] in tests_ids and test_result["result"]:
            success += 1
    percent = 0 if count == 0 else round(success * 100 / count, 2)
    return {"count": count, "percent": percent, "tested": count != 0,
            "result": count != 0 and count == success}
