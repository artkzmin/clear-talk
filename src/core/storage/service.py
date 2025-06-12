from src.core.plan.interfaces import (
    PlanRepositoryInterface,
    UserPlanRepositoryInterface,
)
from src.core.user.interfaces import UserRepositoryInterface
from src.core.message.interfaces import MessageRepositoryInterface
from src.core.storage.interfaces import SessionInterface


class StorageService:
    def __init__(
        self,
        session: SessionInterface,
        plan_factory: type[PlanRepositoryInterface],
        user_plan_factory: type[UserPlanRepositoryInterface],
        user_factory: type[UserRepositoryInterface],
        message_factory: type[MessageRepositoryInterface],
    ):
        self.session = session
        self.plan = plan_factory(session)
        self.user_plan = user_plan_factory(session)
        self.user = user_factory(session)
        self.message = message_factory(session)

    async def __aenter__(self) -> "StorageService":
        self.plan = PlanRepositoryInterface(self.session)
        self.user_plan = UserPlanRepositoryInterface(self.session)
        self.user = UserRepositoryInterface(self.session)
        self.message = MessageRepositoryInterface(self.session)

        return self

    async def __aexit__(self, *args) -> None:
        await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
