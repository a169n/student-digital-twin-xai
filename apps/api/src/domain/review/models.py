from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

# TODO(domain): placeholder actions for the week-6 prototype, not a validated
# taxonomy of teacher responses. factor_looks_wrong feeds the week-7 loop.
Action = Literal["contact_student", "keep_monitoring", "no_action_needed", "factor_looks_wrong"]


class DecisionIn(BaseModel):
    action: Action
    factor: str | None = None
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("note")
    @classmethod
    def _blank_note_is_none(cls, value: str | None) -> str | None:
        return value if value and value.strip() else None

    @model_validator(mode="after")
    def _factor_only_when_flagging(self) -> DecisionIn:
        if (self.action == "factor_looks_wrong") != (self.factor is not None):
            raise ValueError("factor is required for factor_looks_wrong and only for it")
        return self
