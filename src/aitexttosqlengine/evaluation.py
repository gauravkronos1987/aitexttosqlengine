from tqdm.auto import tqdm

def hit_rate(relevance_total):
    if not relevance_total:
        return 0.0

    cnt = 0
    for line in relevance_total:
        if True in line:
            cnt += 1
    return cnt / len(relevance_total)

def mrr(relevance_total):
    if not relevance_total:
        return 0.0

    total_score = 0.0
    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank]:
                total_score += 1 / (rank + 1)
                break
    return total_score / len(relevance_total)


from tqdm import tqdm

import ast

import ast
from tqdm import tqdm


def evaluate(ground_truth, search_function):
    relevance_total = []

    for q in tqdm(ground_truth):
        value = q["relevant_tables"]

        if isinstance(value, str):
            expected_tables = set(ast.literal_eval(value))
        else:
            expected_tables = set(value)

        # This must be outside the if/else block
        results = search_function(q["question"])

        retrieved_tables = []
        seen = set()

        for doc in results:
            table = doc.metadata.get("table")

            if table and table not in seen:
                retrieved_tables.append(table)
                seen.add(table)

        print(f"\nQuestion: {q['question']}")
        print(f"Expected : {sorted(expected_tables)}")
        print(f"Retrieved: {retrieved_tables}")

        relevance = [
            table in expected_tables
            for table in retrieved_tables
        ]

        print(f"Relevance: {relevance}")

        relevance_total.append(relevance)

    metrics = {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
    }

    print(f"\nEvaluation metrics: {metrics}")

    return metrics