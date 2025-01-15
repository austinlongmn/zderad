from .incfile import IncludeFileDirective
from .incimgs import IncludeOutputImagesDirective
from .exec import ExecDirective

directives = {
    "include": IncludeFileDirective,
    "include_images": IncludeOutputImagesDirective,
    "exec": ExecDirective,
}

__all__ = [
    IncludeFileDirective,
    IncludeOutputImagesDirective,
    ExecDirective,
    directives,
]
