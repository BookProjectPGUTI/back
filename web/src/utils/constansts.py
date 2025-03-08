from pydantic import conint

MAX_INT_32 = 2_147_483_647

INT_32 = conint(ge=1, le=MAX_INT_32)
