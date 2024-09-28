"""Models used in API

SPDX-FileCopyrightText: 2023 CERT.at GmbH <https://cert.at/>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    login_token: str
    username: str
