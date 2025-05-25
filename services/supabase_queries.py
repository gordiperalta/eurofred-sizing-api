from config.supabase import supabase_client

def get_u_ach(input_year):
    response = (
        supabase_client
        .table("construction_year")
        .select("*")
        .lte("year", input_year)
        .order("year", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ValueError(f"No data found for construction year ≤ {input_year}. Check Supabase table.")

    row = response.data[0]
    return row["u_average"], row["ach_average"]


def get_orientation_factor(orientation):
    response = (
        supabase_client
        .table("orientation_factor")
        .select("*")
        .eq("orientation", orientation)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise ValueError(f"No orientation factor found for '{orientation}'")

    return response.data[0]["factor"]

