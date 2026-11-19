"""Data contract shared by all modules (the "structured result").

The questionnaire asks for the PLCOm2012 inputs (Tammemägi et al. 2013, Table 2).
The structured result is the ONLY source of facts for the explanation step.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

Race = Literal["white", "black", "hispanic", "asian",
               "american_indian_alaska_native", "native_hawaiian_pacific_islander"]


class Questionnaire(BaseModel):
    age: float = Field(ge=18, le=100)
    race: Race = "white"
    education: int = Field(ge=1, le=6, description="1=<high school ... 6=postgraduate")
    bmi: float = Field(gt=10, lt=80)
    copd: bool = False
    personal_cancer_history: bool = False
    family_history_lung_cancer: bool = False
    smoking_status: Literal["current", "former"]
    cigs_per_day: float = Field(gt=0, le=100)
    smoking_years: float = Field(ge=0, le=90)
    quit_years: float = Field(default=0, ge=0, le=90)
    language: Literal["en", "ro"] = "en"

    @model_validator(mode="after")
    def _check(self) -> "Questionnaire":
        if self.smoking_status == "current" and self.quit_years != 0:
            raise ValueError("current smokers must have quit_years = 0")
        if self.smoking_years + self.quit_years > self.age:
            raise ValueError("years smoked plus years since quitting cannot exceed age")
        return self


# Output names of the TorchXRayVision DenseNet-121 "all" model. Only these may
# reach the explanation: finding names are pasted into the text after the
# verifier has run, so free text here would bypass the verifier.
XrayLabel = Literal["Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Effusion",
                    "Emphysema", "Enlarged Cardiomediastinum", "Fibrosis", "Fracture", "Hernia",
                    "Infiltration", "Lung Lesion", "Lung Opacity", "Mass", "Nodule",
                    "Pleural_Thickening", "Pneumonia", "Pneumothorax"]


class XrayInfo(BaseModel):
    provided: bool = False
    flagged: list[XrayLabel] = []
    not_flagged: list[XrayLabel] = []


class ExplainRequest(BaseModel):
    questionnaire: Questionnaire
    xray: XrayInfo | None = None


class Explanation(BaseModel):
    text: str
    source: Literal["llm", "template"]
    attempts: int
    violations: list[str] = []
