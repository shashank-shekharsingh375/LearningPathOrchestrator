from enum import Enum


class ApprovalStatus(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    UNDER_REVIEW = "Under Review"


class ApprovalManager:
    def decide(self, decision: str, notes: str = "") -> dict:
        normalized = decision.strip().lower()

        if normalized in {"approved", "accept", "yes"}:
            status = ApprovalStatus.APPROVED
        elif normalized in {"rejected", "reject", "no"}:
            status = ApprovalStatus.REJECTED
        else:
            status = ApprovalStatus.UNDER_REVIEW

        return {
            "status": status.value,
            "notes": notes or "Manager review completed.",
        }
