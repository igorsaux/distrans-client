from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LimitsMediaEmoji")


@_attrs_define
class LimitsMediaEmoji:
    """
    Attributes:
        max_dimensions (int):
        max_bytes (int):
        max_animation_frames (int):
        max_animation_duration_ms (int):
    """

    max_dimensions: int
    max_bytes: int
    max_animation_frames: int
    max_animation_duration_ms: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_dimensions = self.max_dimensions

        max_bytes = self.max_bytes

        max_animation_frames = self.max_animation_frames

        max_animation_duration_ms = self.max_animation_duration_ms

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_dimensions": max_dimensions,
                "max_bytes": max_bytes,
                "max_animation_frames": max_animation_frames,
                "max_animation_duration_ms": max_animation_duration_ms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        max_dimensions = d.pop("max_dimensions")

        max_bytes = d.pop("max_bytes")

        max_animation_frames = d.pop("max_animation_frames")

        max_animation_duration_ms = d.pop("max_animation_duration_ms")

        limits_media_emoji = cls(
            max_dimensions=max_dimensions,
            max_bytes=max_bytes,
            max_animation_frames=max_animation_frames,
            max_animation_duration_ms=max_animation_duration_ms,
        )

        limits_media_emoji.additional_properties = d
        return limits_media_emoji

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
