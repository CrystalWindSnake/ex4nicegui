import signe
from signe.core.protocols import ComputedResultProtocol
from typing import (
    TypeVar,
)

T = TypeVar("T")


TReadonlyRef = ComputedResultProtocol[T]
ReadonlyRef = TReadonlyRef[T]
DescReadonlyRef = TReadonlyRef[T]
TGetterOrReadonlyRef = signe.TGetter[T]
_TMaybeRef = signe.TMaybeSignal[T]
TRef = signe.TSignal[T]
Ref = TRef[T]
