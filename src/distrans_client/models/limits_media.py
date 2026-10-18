from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.limits_media_avatar import LimitsMediaAvatar
    from ..models.limits_media_emoji import LimitsMediaEmoji


T = TypeVar("T", bound="LimitsMedia")


@_attrs_define
class LimitsMedia:
    """
    Attributes:
        avatar (LimitsMediaAvatar):
        emoji (LimitsMediaEmoji):
    """

    avatar: LimitsMediaAvatar
    emoji: LimitsMediaEmoji
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar = self.avatar.to_dict()

        emoji = self.emoji.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "avatar": avatar,
                "emoji": emoji,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.limits_media_avatar import LimitsMediaAvatar
        from ..models.limits_media_emoji import LimitsMediaEmoji

        d = dict(src_dict)
        avatar = LimitsMediaAvatar.from_dict(d.pop("avatar"))

        emoji = LimitsMediaEmoji.from_dict(d.pop("emoji"))

        limits_media = cls(
            avatar=avatar,
            emoji=emoji,
        )

        limits_media.additional_properties = d
        return limits_media

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
