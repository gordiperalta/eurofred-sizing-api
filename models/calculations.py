import math

def compute_humidity_ratio_and_load(U, ACH, T_max, RH, area, people, floors, orientation_factor):
    vapor_pressure = RH * 0.61078 * math.exp(17.27 * T_max / (T_max + 237.3))
    humidity_ratio = 0.622 * vapor_pressure / (101.325 - vapor_pressure)
    sensible = U * area * (T_max - 21)
    latent = 67 * people
    ventilation = ACH * area
    load = (sensible + latent + ventilation) * (humidity_ratio * 42 + 0.58) * (0.84 + 0.26 / floors) * orientation_factor / 1000
    return humidity_ratio, load
