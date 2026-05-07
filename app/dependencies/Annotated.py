from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.auth import get_current_user
#from app.core.security import random_account_number


#RandomAccountNumber = Annotated[int, Depends(random_account_number)]

SessionDep = Annotated[AsyncSession, Depends(get_session)]

CurrentUserDep = Annotated[int ,Depends(get_current_user)]