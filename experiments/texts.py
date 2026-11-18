"""Correct explanation drafts and deliberate errors for experiment E1.

These texts are written by hand to TEST the verifier; they are not LLM outputs.
Two sets of error variants exist:
  * DEV variants  - the wording used while the verifier rules were written;
  * TEST variants - other wordings (synonyms, paraphrases) written before the
    first E1 run. The verifier was not changed after seeing E1 results.
Correct drafts include some tricky but correct wordings (negation, "less",
"not a diagnosis") so that false alarms can be measured.
"""
from __future__ import annotations

import random

RISK = [
    "Your chance of lung cancer over the next {plco.horizon} is {plco.display}.",
    "Over the next {plco.horizon}, the model puts your chance of lung cancer at {plco.display}.",
    "Based on your answers, about {plco.display} people like you would get lung cancer "
    "in the next {plco.horizon}.",
    "The calculator estimates a chance of {plco.display} for lung cancer within {plco.horizon}.",
]
QUIT_CURRENT = [
    "If you stop smoking now, your chance {scen.quit_now.y5.when} would be lower than if you "
    "keep smoking: {scen.quit_now.y5}.",
    "Quitting today would give an estimate of {scen.quit_now.y5} {scen.quit_now.y5.when}, which "
    "is less than if you carry on.",
    "Stopping smoking would not make your risk go up; the model gives {scen.quit_now.y7} "
    "{scen.quit_now.y7.when}.",
    "If you give up smoking, the estimate {scen.quit_now.y3.when} is {scen.quit_now.y3}.",
]
QUIT_FORMER = [
    "If you stay smoke-free, the estimate {scen.quit_now.y5.when} is {scen.quit_now.y5}.",
    "Not smoking again keeps the estimate at {scen.quit_now.y5} {scen.quit_now.y5.when}.",
]
CONTINUE_CURRENT = [
    "If you keep smoking as now, it would rise to {scen.continue.y5} {scen.continue.y5.when}.",
    "Continuing to smoke would make the estimate higher: {scen.continue.y7} "
    "{scen.continue.y7.when}.",
    "If you carry on smoking, the chance would not go down; it would be {scen.continue.y3} "
    "{scen.continue.y3.when}.",
]
XRAY = [
    "The computer model flagged {xray.flagged_list} on the X-ray image. A doctor should look at it.",
    "On the X-ray, the model pointed to {xray.flagged_list}. This needs a doctor's review.",
]
CLOSING = [
    "These numbers are estimates from a model, not a diagnosis.",
    "This is not a diagnosis. Please talk to your doctor if you have questions.",
    "A model made these estimates. It cannot tell what will happen to one person.",
]

ERROR_TYPES = ["number", "period", "unit", "direction", "reassurance", "diagnosis", "finding"]

# Each injection is (kind, payload). kind="replace": replace {plco.display}
# sentence part; kind="append": add a sentence.
DEV = {
    "number": [("sub", "{plco.display}", "2%"), ("sub", "{plco.display}", "3 in 100"),
               ("sub", "{plco.display}", "about two in a hundred")],
    "period": [("sub", "{plco.horizon}", "your lifetime"), ("sub", "{plco.horizon}", "each year"),
               ("drop_horizon",)],
    "unit": [("sub", "{plco.display}", "{plco.display} percent"),
             ("sub", "{plco.display}", "{plco.display} per thousand")],
    "direction": [("append", "If you stop smoking now, your risk will go up."),
                  ("append", "Quitting raises your chance of lung cancer.")],
    "reassurance": [("append", "You are safe."), ("append", "There is no risk for you."),
                    ("append", "There is nothing to worry about.")],
    "diagnosis": [("append", "You have lung cancer."),
                  ("append", "You do not have cancer.")],
    "finding": [("append", "The X-ray also shows a nodule."),
                ("append", "There is a mass in your right lung.")],
}

TEST = {
    "number": [("sub", "{plco.display}", "roughly 1 in 50"), ("sub", "{plco.display}", "0.02"),
               ("sub", "{plco.display}", "a few in a hundred"),
               ("append", "That is double the average risk.")],
    "period": [("sub", "{plco.horizon}", "the coming decade"),
               ("sub", "{plco.horizon}", "the rest of your life"),
               ("sub", "{plco.horizon}", "the near future")],
    "unit": [("sub", "{plco.display}", "{plco.display} chance per year of smoking"),
             ("append", "Your odds are worse than average."),
             ("sub", "{plco.display}", "{plco.display} times the normal level")],
    "direction": [("append", "Quitting would make your risk climb."),
                  ("append", "If you give up smoking, the chance gets higher."),
                  ("append", "Stopping smoking will increase your lung cancer risk.")],
    "reassurance": [("append", "You can relax, everything looks fine."),
                    ("append", "Your lungs are in great shape."),
                    ("append", "You will not get lung cancer.")],
    "diagnosis": [("append", "The results show that you are suffering from lung cancer."),
                  ("append", "You've got cancer in your lungs."),
                  ("append", "This confirms a tumour.")],
    "finding": [("append", "There is a small spot on your lung."),
                ("append", "The scan shows a shadow on the left side."),
                ("append", "The X-ray suggests pneumonia.")],
}


def correct_draft(result: dict, rng: random.Random) -> str:
    parts = [rng.choice(RISK)]
    current = result["smoking_status"] == "current"
    parts.append(rng.choice(QUIT_CURRENT if current else QUIT_FORMER))
    if current:
        parts.append(rng.choice(CONTINUE_CURRENT))
    if result["xray"]["provided"] and result["xray"]["flagged"]:
        parts.append(rng.choice(XRAY))
    parts.append(rng.choice(CLOSING))
    return " ".join(parts)


def inject(draft: str, op: tuple) -> str:
    if op[0] == "sub":
        return draft.replace(op[1], op[2], 1)
    if op[0] == "drop_horizon":
        first, _, rest = draft.partition(". ")
        return "Your chance of lung cancer is {plco.display}. " + rest
    if op[0] == "append":
        sents = draft.split(". ")
        sents.insert(1, op[1].rstrip("."))
        return ". ".join(sents)
    raise ValueError(op)
