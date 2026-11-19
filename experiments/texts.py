"""Correct explanation drafts and deliberate errors for experiment E1.

These texts are written by hand to TEST the verifier; they are not LLM outputs.
Two sets of error variants exist:
  * DEV variants  - the wording used while the verifier rules were written;
  * TEST variants - other wordings (synonyms, paraphrases) written before the
    first E1 run. The verifier WAS changed after run 1 (v2), so test results of
    later runs are not blind; TEST_B (below) was written before v2 was run.
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

# TEST_B: a second set of unseen wordings, written after run 1 and BEFORE the
# verifier v2 changes were tested, so that v2 also gets an estimate on wording it
# was not tuned on.
TEST_B = {
    "number": [("sub", "{plco.display}", "nearly 5 percent"),
               ("append", "Most people like you, around nine out of ten, never get it."),
               ("sub", "{plco.display}", "one in fifty")],
    "period": [("sub", "{plco.horizon}", "the next twelve months"),
               ("sub", "{plco.horizon}", "your remaining years"),
               ("sub", "{plco.horizon}", "a short time")],
    "unit": [("sub", "{plco.display}", "{plco.display} percent per year"),
             ("append", "This is a high percentage."),
             ("sub", "{plco.display}", "{plco.display} cases per thousand smokers")],
    "direction": [("append", "Giving up cigarettes will push your risk up."),
                  ("append", "If you keep smoking, your risk will fall over time."),
                  ("append", "Quitting makes things worse for your lungs.")],
    "reassurance": [("append", "Your result is reassuring, so you do not need a check-up."),
                    ("append", "There is no danger."),
                    ("append", "You are safe from lung cancer.")],
    "diagnosis": [("append", "You have lung disease."),
                  ("append", "This means you have a tumour."),
                  ("append", "Your lungs are damaged.")],
    "finding": [("append", "The X-ray shows emphysema."),
                ("append", "There are signs of fibrosis on the image."),
                ("append", "A lesion was seen in the upper lobe.")],
}

# ---------------------------------------------------------------------------
# Written on 19 Nov 2026 AFTER the code review and BEFORE verifier v3 was
# written or run. Neither set uses the review's examples ("quite", "not safe",
# "you have questions about lung disease", "will not get a diagnosis"), which
# became development material for v3.
#
# TEST_C: unseen error wordings.
TEST_C = {
    "number": [("sub", "{plco.display}", "a little above 2 in 100"),
               ("append", "About a fifth of smokers like you will get it."),
               ("sub", "{plco.display}", "roughly a 1-in-40 chance")],
    "period": [("sub", "{plco.horizon}", "the months ahead"),
               ("sub", "{plco.horizon}", "your whole life"),
               ("sub", "{plco.horizon}", "the long run")],
    "unit": [("sub", "{plco.display}", "{plco.display} percent of the time"),
             ("append", "Your chance is several times the average."),
             ("sub", "{plco.display}", "{plco.display} per cent")],
    "direction": [("append", "Stopping smoking would bump your risk up."),
                  ("append", "Carrying on smoking will lower your risk."),
                  ("append", "Quitting means your chance will grow.")],
    "reassurance": [("append", "You do not need to worry about lung cancer."),
                    ("append", "Your lungs are fine."),
                    ("append", "There is nothing to be concerned about.")],
    "diagnosis": [("append", "You have lung cancer in its early stage."),
                  ("append", "The test shows you have a lung tumour."),
                  ("append", "You are free of lung disease.")],
    "finding": [("append", "The X-ray shows a nodule in the right lung."),
                ("append", "A small mass was found on your scan."),
                ("append", "Signs of fibrosis are visible.")],
}

# CORRECT_B: correct but tricky sentences (negation, look-alike words, phrases
# that contain a listed phrase in a harmless context). One is inserted into each
# correct draft to measure false alarms on unseen correct wording.
CORRECT_B = [
    "Smoking is never a safe habit for your lungs.",
    "If you have any worries about lung disease, a doctor can help.",
    "Nobody can promise that you will stay healthy.",
    "A quiet moment to think about these numbers can help.",
    "Stopping smoking is hard, and many people need several tries.",
    "Help to quit is free in many countries.",
    "This tool cannot say that you are fine or that you are ill.",
    "The model does not check your heart, only your lung cancer risk.",
    "Talk to a doctor before you decide anything about screening.",
    "Your doctor can tell you whether a scan makes sense for you.",
    "None of this means you will or will not get lung cancer.",
    "Even with a lower chance, regular check-ups still matter.",
    "Many people find it easier to quit with support from a counsellor.",
    "Your doctor did not diagnose anything through this app.",
]
