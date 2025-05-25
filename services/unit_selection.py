from config.supabase import supabase_client

def select_indoor_units(rooms, cooling_load, total_area):
    all_indoor_units = (
        supabase_client
        .table("eurofred_units")
        .select("code, main_unit_pr_nominal, indoor_type")
        .eq("type", "indoor")
        .execute()
        .data
    )

    results = []
    for room in rooms:
        target_power = 0.98 * cooling_load * room['area'] / total_area
        response = (
            supabase_client
            .table("eurofred_units")
            .select("code, main_unit_pr_nominal, indoor_type")
            .eq("type", "indoor")
            .eq("indoor_type", room['indoor_type'])
            .gte("main_unit_pr_nominal", target_power)
            .order("main_unit_pr_nominal", desc=False)
            .limit(1)
            .execute()
        )

        if not response.data:
            print(f"⚠️ No optimal indoor unit found for room: {room['code']}, using fallback...")
            fallback_units = [u for u in all_indoor_units if u['indoor_type'] == room['indoor_type']]
            if fallback_units:
                selected_unit = min(fallback_units, key=lambda x: x['main_unit_pr_nominal'])
            else:
                selected_unit = min(all_indoor_units, key=lambda x: x['main_unit_pr_nominal'])
        else:
            selected_unit = response.data[0]

        results.append({
            "room_code": room['code'],
            "indoor_unit_code": selected_unit['code'],
            "distance_to_outdoor": room['dist_out_to_in'],
            "distance_to_drain": room['dist_drain']
        })
    return results

def select_outdoor_units(indoor_units, floor_count):
    all_outdoor_units = (
        supabase_client
        .table("eurofred_units")
        .select("code, main_unit_pr_nominal")
        .eq("type", "outdoor")
        .execute()
        .data
    )

    results = []

    for floor in range(1, floor_count + 1):
        floor_units = [u for u in indoor_units if u["room_code"].startswith(f"floor_{floor}_")]

        # Fetch cooling values for the floor's indoor units
        floor_unit_data = []
        for u in floor_units:
            unit_data = (
                supabase_client
                .table("eurofred_units")
                .select("main_unit_pr_nominal")
                .eq("code", u["indoor_unit_code"])
                .execute()
                .data[0]
            )
            floor_unit_data.append({
                "room_code": u["room_code"],
                "cooling_capacity": unit_data["main_unit_pr_nominal"]
            })

        total_cooling = sum(u["cooling_capacity"] for u in floor_unit_data)

        # Find the smallest outdoor unit that can handle the total cooling
        suitable_units = [ou for ou in all_outdoor_units if ou["main_unit_pr_nominal"] >= total_cooling]
        if suitable_units:
            best_unit = min(suitable_units, key=lambda x: x["main_unit_pr_nominal"])
            results.append({
                "floor": floor,
                "outdoor_unit_code": best_unit["code"],
                "paired_units": [u["room_code"] for u in floor_units]
            })
        else:
            print(f"⚠️ No suitable outdoor unit found for floor {floor} needing {total_cooling:.2f} kW")
            # Optionally assign fallback
            fallback = min(all_outdoor_units, key=lambda x: x["main_unit_pr_nominal"])
            results.append({
                "floor": floor,
                "outdoor_unit_code": fallback["code"],
                "paired_units": []  # No match, but logged
            })

    return results
