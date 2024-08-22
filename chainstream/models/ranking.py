import os
import json
from typing import List, Dict
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    FaithulnesswithHHEM,
    answer_relevancy,
    context_utilization,
)
from ragas.metrics.critique import (
    harmfulness,
    maliciousness,
    coherence,
    correctness,
    conciseness,
)


def submit_feedback(feedback_response, llm_key: str) -> bool:
    fb = get_feedback()
    if llm_key not in fb:
        fb[llm_key] = {
            "count": 0,
            "score": 0,
        }
    fb[llm_key]["count"] += 1
    fb[llm_key]["score"] += (
        ["😞", "🙁", "😐", "🙂", "😀"].index(feedback_response["score"]) + 1
    ) / 5
    return set_feedback(fb)


def calc_score_from_feedback(llm_key: str) -> float:
    fb = get_feedback()
    if llm_key not in fb:
        return 0.6
    return fb[llm_key]["score"] / fb[llm_key]["count"]


def get_feedback():
    path = (
        os.environ.get("PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/"))
        + "feedback.json"
    )
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        set_feedback({})
        return get_feedback()


def set_feedback(obj) -> bool:
    path = (
        os.environ.get("PROJECT_DATA_DIR", os.path.expanduser("~/Downloads/3S-SE-AI/"))
        + "feedback.json"
    )
    with open(path, "w") as json_file:
        json.dump(obj, json_file)
    return True


def calc_score(question, answer, contexts, embeddings, llm) -> float:
    try:
        metrics_data = Dataset.from_dict(
            {
                "question": [question],
                "answer": [answer],
                "contexts": [contexts],
            }
        )
        scores = evaluate(
            metrics_data,
            metrics=[
                FaithulnesswithHHEM(),
                answer_relevancy,
                context_utilization,
                harmfulness,
                maliciousness,
                coherence,
                correctness,
                conciseness,
            ],
            embeddings=embeddings,
            llm=llm,
        )
        return sum(scores.values())
    except BaseException as e:
        print(e)
        return float(0)


def reranked(answers: List[Dict], embeddings=None, config=None) -> List[Dict]:
    if embeddings is not None and config is not None:
        scores = [
            calc_score(
                question=answer["answer"]["question"],
                answer=answer["answer"]["answer"],
                contexts=[doc.page_content for doc in answer["answer"]["context"]],
                embeddings=embeddings,
                llm=config["llms"][answer["llm_key"]]["model"],
            )
            + calc_score_from_feedback(answer["llm_key"])
            for answer in answers
        ]
    else:
        scores = [calc_score_from_feedback(answer["llm_key"]) for answer in answers]
    return sorted(answers, key=lambda obj: scores[answers.index(obj)], reverse=False)
