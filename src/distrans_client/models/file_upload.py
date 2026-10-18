from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FileUpload")


@_attrs_define
class FileUpload:
    """
    Attributes:
        id (str): Decimal string of a 64-bit snowflake ID (JS BigInt compatible)
        name (str): Original file name, within `api.files.max_name_codepoints` codepoints.
        size (int): Size of the stored object in bytes.
        content_type (str): MIME type of the stored object; always `image/webp` for re-encoded raster uploads
            (WebP/GIF/PNG/JPEG), otherwise the request `Content-Type`.
        hash_ (str): Hex SHA-256 of the bytes and the object key suffix (`files/{hash}`).
        public_url (None | str): `{files.s3.public_base_url}/files/{hash}`; null when storage is disabled. Not access-
            controlled: anyone with the URL can fetch the object. The object carries a `Content-Disposition` with the
            sanitized original `name`, so navigating to this URL downloads the file under its original name.
    """

    id: str
    name: str
    size: int
    content_type: str
    hash_: str
    public_url: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        size = self.size

        content_type = self.content_type

        hash_ = self.hash_

        public_url: None | str
        public_url = self.public_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "size": size,
                "content_type": content_type,
                "hash": hash_,
                "public_url": public_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        size = d.pop("size")

        content_type = d.pop("content_type")

        hash_ = d.pop("hash")

        def _parse_public_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        public_url = _parse_public_url(d.pop("public_url"))

        file_upload = cls(
            id=id,
            name=name,
            size=size,
            content_type=content_type,
            hash_=hash_,
            public_url=public_url,
        )

        file_upload.additional_properties = d
        return file_upload

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
