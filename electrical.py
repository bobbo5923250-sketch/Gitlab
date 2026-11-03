def analyze_dc(voltage_v, resistance_ohm):
    if resistance_ohm <= 0:
        raise ValueError("Resistance must be greater than zero.")
    current_a = voltage_v / resistance_ohm
    power_w = voltage_v * current_a
    return {"current_a": current_a, "power_w": power_w}


def analyze_circuit(voltage_v, resistances_ohm, connection):
    if not resistances_ohm:
        raise ValueError("Enter at least one resistor.")
    if any(resistance <= 0 for resistance in resistances_ohm):
        raise ValueError("All resistances must be greater than zero.")
    if connection not in ("series", "parallel"):
        raise ValueError("Connection must be 'series' or 'parallel'.")

    if connection == "series":
        equivalent_resistance = sum(resistances_ohm)
    else:
        equivalent_resistance = 1 / sum(1 / resistance for resistance in resistances_ohm)

    total = analyze_dc(voltage_v, equivalent_resistance)
    components = []
    for resistance in resistances_ohm:
        if connection == "series":
            current = total["current_a"]
            voltage = current * resistance
        else:
            voltage = voltage_v
            current = voltage / resistance
        components.append({
            "voltage_v": voltage,
            "current_a": current,
            "power_w": voltage * current,
        })

    return {
        "equivalent_resistance_ohm": equivalent_resistance,
        **total,
        "components": components,
    }


def main():
    print("DC Circuit Calculator")
    voltage_v = float(input("Supply voltage (V): "))
    connection = input("Connection (series/parallel): ").strip().lower()
    resistances_ohm = [
        float(value.strip())
        for value in input("Resistances in ohms (comma-separated): ").split(",")
    ]

    result = analyze_circuit(voltage_v, resistances_ohm, connection)
    print(f"\nEquivalent resistance: {result['equivalent_resistance_ohm']:.4g} ohm")
    print(f"Total current: {result['current_a']:.4g} A")
    print(f"Total power: {result['power_w']:.4g} W")
    for index, component in enumerate(result["components"], start=1):
        print(
            f"R{index}: {component['voltage_v']:.4g} V, "
            f"{component['current_a']:.4g} A, "
            f"{component['power_w']:.4g} W"
        )


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Input error: {error}")