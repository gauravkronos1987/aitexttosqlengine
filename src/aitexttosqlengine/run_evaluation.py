import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from aitexttosqlengine.evaluation import evaluate
from aitexttosqlengine.search import SchemaSearcher

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GROUND_TRUTH_FILE = PROJECT_ROOT / "data" / "ground_truth-new.csv"
print(GROUND_TRUTH_FILE)
METRICS_FILE = PROJECT_ROOT / "evaluation_metrics.json"


def run_evaluation() -> dict:
    df = pd.read_csv(GROUND_TRUTH_FILE)
    ground_truth = df.to_dict(orient="records")

    searcher = SchemaSearcher()

    metrics = evaluate(
        ground_truth=ground_truth,
        search_function=searcher.search,
    )

    result = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "evaluated_questions": len(ground_truth),
        "hit_rate": metrics["hit_rate"],
        "mrr": metrics["mrr"],
    }

    METRICS_FILE.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print("Evaluation completed")
    print(json.dumps(result, indent=2))

    return result


if __name__ == "__main__":
    run_evaluation()