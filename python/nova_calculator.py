# This is a simple Austrian NoVA calculator
from collections import namedtuple
from decimal import Decimal

VAT = 0.2
QUANTIZATION_OBJECT = Decimal("1.00")

Parameter = namedtuple(
    "Parameter",
    "co2_deduction deduction_amount co2_limit additional_costs tax_rate_max",
)

PARAMETERS_LIST = {
    2021: Parameter(
        112,
        350,
        200,
        Decimal("50.00"),
        Decimal("0.50"),
    ),
    2022: Parameter(
        107,
        350,
        185,
        Decimal("60.00"),
        Decimal("0.60"),
    ),
    2023: Parameter(
        102,
        350,
        170,
        Decimal("70.00"),
        Decimal("0.70"),
    ),
    2024: Parameter(
        97,
        350,
        155,
        Decimal("80.00"),
        Decimal("0.80"),
    ),
}


def get_nova_rate(
    *,
    year: int = None,
    co2_value: int = None,
):
    if not year or not co2_value:
        return None
    parameters = PARAMETERS_LIST.get(year)
    nova_rate = Decimal(
        f"{min(max(co2_value-parameters.co2_deduction, 0)/500, parameters.tax_rate_max)*100}"
    ).quantize(QUANTIZATION_OBJECT)
    return nova_rate


def read_nova_parameters(
    *,
    year: int = None,
    car_price: Decimal | int | float = None,
    co2_value: int = None,
    vat: float = None,
):
    if not year:
        year = int(input("Please enter the year for calculation: "))
    if not PARAMETERS_LIST.get(year):
        raise ValueError(f"Parameters for year {year} are not available!")
    if not isinstance(vat, (int, float)) and not vat:
        vat = int(
            input("Please enter the vat for calculation: ").replace(",", ".")
        )
    vat = Decimal(vat)
    if not car_price:
        car_price = float(input("Please enter car's price: ").replace(",", "."))
    car_price = Decimal(car_price)
    if not isinstance(co2_value, (int, float)) and not co2_value:
        co2_value = float(
            input("Please enter car's co2 value: ").replace(",", ".")
        )
    parameters = PARAMETERS_LIST.get(year)
    nova_rate = Decimal(
        f"{min(max(co2_value-parameters.co2_deduction, 0)/500, parameters.tax_rate_max)}"
    ).quantize(QUANTIZATION_OBJECT)
    bonus_malus = Decimal(
        Decimal(co2_value - parameters.co2_limit) * parameters.additional_costs
        if co2_value > parameters.co2_limit
        else 0
    )
    return car_price, co2_value, parameters, vat, nova_rate, bonus_malus


def calculate_nova_gross(
    *,
    year: int = None,
    net_price: Decimal | int | float = None,
    co2_value: int = None,
    vat: float = None,
) -> Decimal:
    """Calculate the NoVA gross price based on car's net price.
    >>> calculate_nova_gross(year=2022, net_price=17000, co2_value=0, vat=0.2)
    Decimal('20400.00')
    >>> calculate_nova_gross(year=2022, net_price=17000, co2_value=110, vat=0.2)
    Decimal('20400.00')
    >>> calculate_nova_gross(year=2022, net_price=17000, co2_value=185, vat=0.2)
    Decimal('22770.00')
    >>> calculate_nova_gross(year=2022, net_price=17000, co2_value=200, vat=0.2)
    Decimal('24180.00')
    >>> calculate_nova_gross(year=2022, net_price=17000, co2_value=250, vat=0.2)
    Decimal('28880.00')
    >>> calculate_nova_gross(year=2020, net_price=17000, co2_value=250, vat=0.2)
    Traceback (most recent call last):
    ...
    ValueError: Parameters for year 2020 are not available!
    """

    (
        net_price,
        co2_value,
        parameters,
        vat,
        nova_rate,
        bonus_malus,
    ) = read_nova_parameters(
        year=year, car_price=net_price, co2_value=co2_value, vat=vat
    )
    gross_price = (net_price * (1 + vat)) + max(
        net_price * nova_rate + bonus_malus - parameters.deduction_amount, 0
    )
    return Decimal(f"{gross_price}").quantize(QUANTIZATION_OBJECT)


def calculate_nova_net(
    *,
    year: int = None,
    gross_price: Decimal | int | float = None,
    co2_value: int = None,
    vat: float = None,
) -> Decimal:
    """Calculate the car's net price based on car's NoVA gross price.
    >>> calculate_nova_net(year=2022, gross_price=20400, co2_value=0, vat=0.2)
    Decimal('17000.00')
    >>> calculate_nova_net(year=2022, gross_price=20400, co2_value=110, vat=0.2)
    Decimal('17000.00')
    >>> calculate_nova_net(year=2022, gross_price=22770, co2_value=185, vat=0.2)
    Decimal('17000.00')
    >>> calculate_nova_net(year=2022, gross_price=24180, co2_value=200, vat=0.2)
    Decimal('17000.00')
    >>> calculate_nova_net(year=2022, gross_price=28880, co2_value=250, vat=0.2)
    Decimal('17000.00')
    >>> calculate_nova_net(year=2020, gross_price=17000, co2_value=250, vat=0.2)
    Traceback (most recent call last):
    ...
    ValueError: Parameters for year 2020 are not available!
    """

    (
        gross_price,
        co2_value,
        parameters,
        vat,
        nova_rate,
        bonus_malus,
    ) = read_nova_parameters(
        year=year, car_price=gross_price, co2_value=co2_value, vat=vat
    )
    for deduction_amount in range(
        0, (parameters.deduction_amount * 100) + 1, 1
    ):
        deduction_amount /= 100
        deduction_amount = Decimal(deduction_amount)
        net_price = (gross_price - bonus_malus + deduction_amount) / (
            1 + vat + nova_rate
        )
        nova_value = Decimal(f"{net_price * nova_rate}").quantize(
            QUANTIZATION_OBJECT
        )
        check_sum = nova_value + bonus_malus - deduction_amount
        if check_sum == 0 or (
            check_sum < 0 and check_sum == nova_value - deduction_amount
        ):
            return net_price.quantize(QUANTIZATION_OBJECT)
    return Decimal(
        (gross_price + parameters.deduction_amount - bonus_malus)
        / (1 + vat + nova_rate)
    ).quantize(QUANTIZATION_OBJECT)


def main():
    available_modes = {"n": "[n]et>gross", "g": "[g]ross>net"}
    while chosen_mode := input(
        f"Please choose calculation mode: {available_modes}: "
    ):
        print("---------------------------")
        if chosen_mode not in available_modes.keys():
            print(f"Unknown mode: {chosen_mode}")
            continue
        if chosen_mode == "n":
            car_gross_price = calculate_nova_gross()
            print(f"\nThe gross price is: {car_gross_price:.2f}")
        if chosen_mode == "g":
            car_net_price = calculate_nova_net()
            print(f"\nThe net price is: {car_net_price:.2f}")
        print("---------------------------")
    print("Thanks for using the NoVA calculator!")


if __name__ == "__main__":
    main()
