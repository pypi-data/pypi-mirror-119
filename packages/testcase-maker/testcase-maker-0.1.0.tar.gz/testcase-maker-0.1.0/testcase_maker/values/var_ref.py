from typing import Any, TYPE_CHECKING

import attr

from testcase_maker.values.base import BaseValue

if TYPE_CHECKING:
    from testcase_maker.core import Resolver


@attr.define()
class VarRef(BaseValue):
    var_name: Any = attr.ib()

    def generate(self, resolver: "Resolver") -> Any:
        var_name = resolver.resolve(self.var_name)
        return resolver.get_value(var_name)
