"""Contains polygon parameters for each polygon representing a geographic area in geojson format
and a dict of provider names and their associated service areas

This is to be used as data input for test cases."""

kubwa_polygon = [
    [
        [7.328224182128906, 9.172601695217214],
        [7.319297790527343, 9.172093296027171],
        [7.316036224365234, 9.163111456935153],
        [7.3107147216796875, 9.146163972348372],
        [7.322044372558593, 9.144299699743243],
        [7.33062744140625, 9.139045788056714],
        [7.355003356933594, 9.138537340876388],
        [7.3572349548339835, 9.143791260065337],
        [7.358436584472656, 9.150570396043845],
        [7.356719970703125, 9.160569385757544],
        [7.352085113525391, 9.169042885592111],
        [7.328224182128906, 9.172601695217214],
    ]
]


dutse_polygon = [
    [
        [7.36307144165039, 9.15260411164787],
        [7.3534584045410165, 9.149384056571519],
        [7.3546600341796875, 9.137859410173567],
        [7.375946044921875, 9.12497848177753],
        [7.384357452392577, 9.133961283596275],
        [7.384185791015625, 9.146672408636736],
        [7.37680435180664, 9.154976765152881],
        [7.36307144165039, 9.15260411164787],
    ]
]


gwarinpa_polygon = [
    [
        [7.405643463134766, 9.118029366685613],
        [7.373027801513672, 9.123792057073985],
        [7.366161346435548, 9.08548537081665],
        [7.396202087402343, 9.075314765358186],
        [7.409076690673829, 9.07667086275516],
        [7.413368225097656, 9.089723037902536],
        [7.424354553222655, 9.104808725563043],
        [7.405643463134766, 9.118029366685613],
    ]
]

jahi_polygon = [
    [
        [7.435169219970702, 9.11641918656483],
        [7.428388595581054, 9.117097158027109],
        [7.426328659057616, 9.105062973274334],
        [7.418088912963867, 9.094553917213506],
        [7.411823272705077, 9.086671922653913],
        [7.464780807495117, 9.090231554583605],
        [7.46744155883789, 9.105401969941486],
        [7.4458980560302725, 9.116842918879613],
        [7.435169219970702, 9.11641918656483],
    ]
]

maitama_polygon = [
    [
        [7.475337982177735, 9.09574043900164],
        [7.4994564056396475, 9.072094013494144],
        [7.509756088256836, 9.09150284312696],
        [7.504005432128906, 9.099723733373704],
        [7.480659484863281, 9.110910620720261],
        [7.475337982177735, 9.09574043900164],
    ]
]

providers = [
    {
        "name": "GIGM",
        "email": "gigm@gigm.com",
        "phone_number": "0812345678",
        "language": "en",
        "currency": "ngn",
    },
    {
        "name": "Bolt",
        "email": "bolt@bolt.ng",
        "phone_number": "0812345677",
        "language": "en",
        "currency": "ngn",
    },
    {
        "name": "YSG",
        "email": "ysg@ysg.com",
        "phone_number": "0812345676",
        "language": "fr",
        "currency": "usd",
    },
    {
        "name": "GAM",
        "email": "gam@gam.com",
        "phone_number": "0812345675",
        "language": "es",
        "currency": "aud",
    },
    {
        "name": "ABC",
        "email": "abc@abc.com",
        "phone_number": "0812345674",
        "language": "en",
        "currency": "eur",
    },
]

"""kubwa, dutse, gwarinpa, jahi, maitama"""
provider_x_service_areas = {
    "GIGM": [
        {
            "name": "gigm_kubwa",
            "price": 500,
            "polygon": {"type": "Polygon", "coordinates": kubwa_polygon},
        },
        {
            "name": "gigm_dutse",
            "price": 600,
            "polygon": {"type": "Polygon", "coordinates": dutse_polygon},
        },
        {
            "name": "gigm_gwarinpa",
            "price": 1000,
            "polygon": {"type": "Polygon", "coordinates": gwarinpa_polygon},
        },
    ],
    "Bolt": [
        {
            "name": "bolt_dutse",
            "price": 700,
            "polygon": {"type": "Polygon", "coordinates": dutse_polygon},
        },
        {
            "name": "bolt_gwarinpa",
            "price": 1500,
            "polygon": {"type": "Polygon", "coordinates": gwarinpa_polygon},
        },
        {
            "name": "bolt_jahi",
            "price": 500,
            "polygon": {"type": "Polygon", "coordinates": jahi_polygon},
        },
    ],
    "YSG": [
        {
            "name": "ysg_gwarinpa",
            "price": 800,
            "polygon": {"type": "Polygon", "coordinates": gwarinpa_polygon},
        },
        {
            "name": "ysg_jahi",
            "price": 750,
            "polygon": {"type": "Polygon", "coordinates": jahi_polygon},
        },
        {
            "name": "ysg_maitama",
            "price": 1700,
            "polygon": {"type": "Polygon", "coordinates": maitama_polygon},
        },
    ],
    "GAM": [
        {
            "name": "gam_jahi",
            "price": 900,
            "polygon": {"type": "Polygon", "coordinates": jahi_polygon},
        },
        {
            "name": "gam_maitama",
            "price": 1900,
            "polygon": {"type": "Polygon", "coordinates": maitama_polygon},
        },
        {
            "name": "gam_kubwa",
            "price": 400,
            "polygon": {"type": "Polygon", "coordinates": kubwa_polygon},
        },
    ],
    "ABC": [
        {
            "name": "abc_maitama",
            "price": 2200,
            "polygon": {"type": "Polygon", "coordinates": maitama_polygon},
        },
        {
            "name": "abc_kubwa",
            "price": 950,
            "polygon": {"type": "Polygon", "coordinates": kubwa_polygon},
        },
        {
            "name": "abc_dutse",
            "price": 500,
            "polygon": {"type": "Polygon", "coordinates": dutse_polygon},
        },
    ],
}
