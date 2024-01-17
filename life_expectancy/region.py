from enum import Enum, auto, unique


@unique
class Region(Enum):
    """An enumerate for available regions in the life expectancy scope."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """A redefinition of the staticmethod that is used to determine the next value returned by
        auto, in this case the name of the country itself.

        Lazily stolen from: https://docs.python.org/3/library/enum.html#enum.Enum._generate_next_value_

        Args:
            name (_type_): The name of the member being defined.
            start (_type_): The start value for the Enum; the default is 1.
            count (_type_): The number of members currently defined, not including this one.
            last_values (_type_): A list of the previous values.

        Returns:
            str: The name of the region.
        """
        return name

    @classmethod
    def get_country_list(cls) -> list:
        """Returns a list of actual countries.

        Returns:
            list: the list of available countries in Region.
        """
        return [region.name for region in Region if len(region.name) == 2]

    AL = auto()
    AM = auto()
    AT = auto()
    AZ = auto()
    BE = auto()
    BG = auto()
    BY = auto()
    CH = auto()
    CY = auto()
    CZ = auto()
    DE = auto()
    DE_TOT = auto()
    DK = auto()
    EA18 = auto()
    EA19 = auto()
    EE = auto()
    EEA30_2007 = auto()
    EEA31 = auto()
    EFTA = auto()
    EL = auto()
    ES = auto()
    EU27_2007 = auto()
    EU27_2020 = auto()
    EU28 = auto()
    FI = auto()
    FR = auto()
    FX = auto()
    GE = auto()
    HR = auto()
    HU = auto()
    IE = auto()
    IS = auto()
    IT = auto()
    LI = auto()
    LT = auto()
    LU = auto()
    LV = auto()
    MD = auto()
    ME = auto()
    MK = auto()
    MT = auto()
    NL = auto()
    NO = auto()
    PL = auto()
    PT = auto()
    RO = auto()
    RS = auto()
    RU = auto()
    SE = auto()
    SI = auto()
    SK = auto()
    SM = auto()
    TR = auto()
    UA = auto()
    UK = auto()
    XK = auto()
