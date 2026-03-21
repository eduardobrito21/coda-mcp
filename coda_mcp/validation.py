import json
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, cast, overload

from pydantic import TypeAdapter, ValidationError
from pydantic_core import ErrorDetails

# Keyed by schema type. Bounded by distinct types in the codebase, not by data volume.
_type_adapter_cache: dict[Any, TypeAdapter[Any]] = {}


@overload
def validate_pydantic[T](
    schema: type[T],
    values: Any,
    strict: bool | None = None,
    from_attributes: bool | None = None,
    context: dict[str, Any] | None = None,
    print_errors: bool = True,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> T: ...


@overload
def validate_pydantic[T](
    schema: T,
    values: Any,
    strict: bool | None = None,
    from_attributes: bool | None = None,
    context: dict[str, Any] | None = None,
    print_errors: bool = True,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> T: ...


def validate_pydantic(
    schema: Any,
    values: Any,
    strict: bool | None = None,
    from_attributes: bool | None = None,
    context: dict[str, Any] | None = None,
    print_errors: bool = True,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> Any:
    try:
        return _get_type_adapter(schema).validate_python(
            values,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            by_alias=by_alias,
            by_name=by_name,
        )
    except ValidationError as err:
        if print_errors:
            print("Errors", _serialize_pydantic_validation_error(err))
        raise err


if TYPE_CHECKING:
    validate_pydantic_as_cast = cast
else:

    def validate_pydantic_as_cast(
        schema: Any,
        values: Any,
    ) -> Any:
        return validate_pydantic(schema, values)


def _get_type_adapter(schema: Any) -> TypeAdapter[Any]:
    adapter = _type_adapter_cache.get(schema)
    if adapter is None:
        adapter = TypeAdapter(schema)
        _type_adapter_cache[schema] = adapter
    return adapter


def _serialize_pydantic_validation_error(err: ValidationError) -> str:
    errors = [{**error.copy()} for error in err.errors()]
    parsed_errors = _serialize_pydantic_error_dicts(errors)
    return json.dumps(parsed_errors, indent=2)


def _serialize_pydantic_error_dicts(
    errors: Sequence[dict[str, Any]] | list[ErrorDetails],
) -> dict[str, str]:
    errs: dict[str, str] = {}
    error_details = cast(list[ErrorDetails], errors)
    for err in error_details:
        loc = err.get("loc", [])
        path = ".".join(map(str, loc)) if not isinstance(loc, str) else str(loc)
        errs[path] = err.get("msg", "")
    return errs
