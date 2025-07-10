from src.core.plan.entities import UserPlan


class RemainingUserPlan(UserPlan):
    remaining_days_count: int | None
    remaining_messages_count: int | None
