from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.embed_type import EmbedType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.embed_author import EmbedAuthor
    from ..models.embed_field import EmbedField
    from ..models.embed_footer import EmbedFooter
    from ..models.embed_image import EmbedImage
    from ..models.embed_thumbnail import EmbedThumbnail
    from ..models.embed_video import EmbedVideo


T = TypeVar("T", bound="Embed")


@_attrs_define
class Embed:
    """A rich embed. Validation is strict: when a sub-object is present its required fields (`footer.text`, `author.name`,
    `image`/`thumbnail`/`video.url`, `field.name`/`field.value`) must be present too. Text fields are NFKC-normalized
    and message-text forbidden codepoints are stripped; URLs are bounded by `api.embeds.max_url_codepoints` and do not
    count towards `api.embeds.max_total_codepoints`. At most `api.messages.max_embeds` embeds are accepted per message.

        Attributes:
            type_ (EmbedType | Unset):  Default: EmbedType.RICH.
            title (None | str | Unset):
            description (None | str | Unset):
            url (None | str | Unset):
            timestamp (int | None | Unset): Unix epoch, milliseconds
            color (int | None | Unset):
            footer (EmbedFooter | None | Unset):
            image (EmbedImage | None | Unset):
            thumbnail (EmbedThumbnail | None | Unset):
            video (EmbedVideo | None | Unset):
            author (EmbedAuthor | None | Unset):
            fields (list[EmbedField] | Unset):
    """

    type_: EmbedType | Unset = EmbedType.RICH
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    url: None | str | Unset = UNSET
    timestamp: int | None | Unset = UNSET
    color: int | None | Unset = UNSET
    footer: EmbedFooter | None | Unset = UNSET
    image: EmbedImage | None | Unset = UNSET
    thumbnail: EmbedThumbnail | None | Unset = UNSET
    video: EmbedVideo | None | Unset = UNSET
    author: EmbedAuthor | None | Unset = UNSET
    fields: list[EmbedField] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.embed_author import EmbedAuthor
        from ..models.embed_footer import EmbedFooter
        from ..models.embed_image import EmbedImage
        from ..models.embed_thumbnail import EmbedThumbnail
        from ..models.embed_video import EmbedVideo

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        timestamp: int | None | Unset
        if isinstance(self.timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = self.timestamp

        color: int | None | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        footer: dict[str, Any] | None | Unset
        if isinstance(self.footer, Unset):
            footer = UNSET
        elif isinstance(self.footer, EmbedFooter):
            footer = self.footer.to_dict()
        else:
            footer = self.footer

        image: dict[str, Any] | None | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, EmbedImage):
            image = self.image.to_dict()
        else:
            image = self.image

        thumbnail: dict[str, Any] | None | Unset
        if isinstance(self.thumbnail, Unset):
            thumbnail = UNSET
        elif isinstance(self.thumbnail, EmbedThumbnail):
            thumbnail = self.thumbnail.to_dict()
        else:
            thumbnail = self.thumbnail

        video: dict[str, Any] | None | Unset
        if isinstance(self.video, Unset):
            video = UNSET
        elif isinstance(self.video, EmbedVideo):
            video = self.video.to_dict()
        else:
            video = self.video

        author: dict[str, Any] | None | Unset
        if isinstance(self.author, Unset):
            author = UNSET
        elif isinstance(self.author, EmbedAuthor):
            author = self.author.to_dict()
        else:
            author = self.author

        fields: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.fields, Unset):
            fields = []
            for fields_item_data in self.fields:
                fields_item = fields_item_data.to_dict()
                fields.append(fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if url is not UNSET:
            field_dict["url"] = url
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if color is not UNSET:
            field_dict["color"] = color
        if footer is not UNSET:
            field_dict["footer"] = footer
        if image is not UNSET:
            field_dict["image"] = image
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if video is not UNSET:
            field_dict["video"] = video
        if author is not UNSET:
            field_dict["author"] = author
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.embed_author import EmbedAuthor
        from ..models.embed_field import EmbedField
        from ..models.embed_footer import EmbedFooter
        from ..models.embed_image import EmbedImage
        from ..models.embed_thumbnail import EmbedThumbnail
        from ..models.embed_video import EmbedVideo

        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: EmbedType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = EmbedType(_type_)

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_timestamp(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        timestamp = _parse_timestamp(d.pop("timestamp", UNSET))

        def _parse_color(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_footer(data: object) -> EmbedFooter | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                footer_type_1 = EmbedFooter.from_dict(data)

                return footer_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbedFooter | None | Unset, data)

        footer = _parse_footer(d.pop("footer", UNSET))

        def _parse_image(data: object) -> EmbedImage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                image_type_1 = EmbedImage.from_dict(data)

                return image_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbedImage | None | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_thumbnail(data: object) -> EmbedThumbnail | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                thumbnail_type_1 = EmbedThumbnail.from_dict(data)

                return thumbnail_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbedThumbnail | None | Unset, data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail", UNSET))

        def _parse_video(data: object) -> EmbedVideo | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                video_type_1 = EmbedVideo.from_dict(data)

                return video_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbedVideo | None | Unset, data)

        video = _parse_video(d.pop("video", UNSET))

        def _parse_author(data: object) -> EmbedAuthor | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                author_type_1 = EmbedAuthor.from_dict(data)

                return author_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(EmbedAuthor | None | Unset, data)

        author = _parse_author(d.pop("author", UNSET))

        _fields = d.pop("fields", UNSET)
        fields: list[EmbedField] | Unset = UNSET
        if _fields is not UNSET:
            fields = []
            for fields_item_data in _fields:
                fields_item = EmbedField.from_dict(fields_item_data)

                fields.append(fields_item)

        embed = cls(
            type_=type_,
            title=title,
            description=description,
            url=url,
            timestamp=timestamp,
            color=color,
            footer=footer,
            image=image,
            thumbnail=thumbnail,
            video=video,
            author=author,
            fields=fields,
        )

        embed.additional_properties = d
        return embed

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
