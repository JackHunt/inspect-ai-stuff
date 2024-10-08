from inspect_ai import Task, eval, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.scorer import answer
from inspect_ai.solver import multiple_choice, system_message


def record_to_sample(record):
    # read the labels and text
    choices = record["choices"]
    choices = dict(zip(choices["label"], choices["text"]))

    # determine the target then normalize to letter
    answerKey = record["answerKey"]
    target = list(choices.keys()).index(answerKey)
    target = chr(ord("A") + int(target))

    # return sample
    return Sample(
        input=record["question"], choices=list(choices.values()), target=target
    )


def arc_task(dataset_name):
    return Task(
        dataset=hf_dataset(
            path="allenai/ai2_arc",
            name=dataset_name,
            split="test",
            sample_fields=record_to_sample,
        ),
        plan=multiple_choice(),
        scorer=answer("letter"),
    )


@task
def easy():
    return arc_task("ARC-Easy")


@task
def challenge():
    return arc_task("ARC-Challenge")
