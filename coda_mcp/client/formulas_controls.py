from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    ControlDetail,
    ControlsListQuery,
    ControlsListResponse,
    FormulaDetail,
    FormulasListQuery,
    FormulasListResponse,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class FormulasControlsClient(CodaRequestMixin):
    """Named formulas and controls in a doc ([Coda API — Formulas & controls](https://coda.io/developers/apis/v1#))."""

    http: httpx.AsyncClient
    base_url: str

    async def get_formulas_list(
        self,
        doc_id: str,
        query: FormulasListQuery | None = None,
        *,
        api_key: str,
    ) -> FormulasListResponse:
        response = await self.http.get(
            self.url(f"/docs/{quote(doc_id, safe='')}/formulas"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FormulasListResponse, response.json())

    async def get_formula(
        self, doc_id: str, formula_id_or_name: str, *, api_key: str
    ) -> FormulaDetail:
        seg = quote(formula_id_or_name, safe="")
        response = await self.http.get(
            self.url(f"/docs/{quote(doc_id, safe='')}/formulas/{seg}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FormulaDetail, response.json())

    async def get_controls_list(
        self,
        doc_id: str,
        query: ControlsListQuery | None = None,
        *,
        api_key: str,
    ) -> ControlsListResponse:
        response = await self.http.get(
            self.url(f"/docs/{quote(doc_id, safe='')}/controls"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(ControlsListResponse, response.json())

    async def get_control(
        self, doc_id: str, control_id_or_name: str, *, api_key: str
    ) -> ControlDetail:
        seg = quote(control_id_or_name, safe="")
        response = await self.http.get(
            self.url(f"/docs/{quote(doc_id, safe='')}/controls/{seg}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(ControlDetail, response.json())
