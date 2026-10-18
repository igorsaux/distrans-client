from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsFiles")


@_attrs_define
class LimitsFiles:
    """
    Attributes:
        max_name_codepoints (int):
        max_size (int):
        whitelist (list[str] | None): MIME patterns accepted by `POST /api/files`, mirroring `files.whitelist`. `null`
            allows every type, an empty array allows none. An exact `type/subtype` matches that type; a `<type>/*` entry
            (e.g. `text/*`) matches any subtype of that type.
        public_base_urls (list[str]): Origins from which files are served (`files.s3.public_base_url`); empty when
            storage is disabled. Use these to build a Content-Security-Policy `img-src` / `media-src` allowlist. Served with
            the HTML document, not by the API. Files are served cross-origin; the files origin/CDN should add `X-Content-
            Type-Options: nosniff`, `Content-Security-Policy: sandbox; default-src 'none'; frame-ancestors 'none'`, `Cross-
            Origin-Resource-Policy: cross-origin` and `Referrer-Policy: no-referrer`, since the stored `Content-Type` of
            passthrough types is client-declared.
    """

    max_name_codepoints: int
    max_size: int
    whitelist: list[str] | None
    public_base_urls: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_name_codepoints = self.max_name_codepoints

        max_size = self.max_size

        whitelist: list[str] | None
        if isinstance(self.whitelist, list):
            whitelist = self.whitelist

        else:
            whitelist = self.whitelist

        public_base_urls = self.public_base_urls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_name_codepoints": max_name_codepoints,
                "max_size": max_size,
                "whitelist": whitelist,
                "public_base_urls": public_base_urls,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_name_codepoints = d.pop("max_name_codepoints")

        max_size = d.pop("max_size")

        def _parse_whitelist(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                whitelist_type_0 = cast(list[str], data)

                return whitelist_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        whitelist = _parse_whitelist(d.pop("whitelist"))

        public_base_urls = cast(list[str], d.pop("public_base_urls"))

        limits_files = cls(
            max_name_codepoints=max_name_codepoints,
            max_size=max_size,
            whitelist=whitelist,
            public_base_urls=public_base_urls,
        )

        limits_files.additional_properties = d
        return limits_files

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
