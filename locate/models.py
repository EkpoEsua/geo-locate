from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case

# Create your models here.


class Provider(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)

    # Language is encoded in ISO 639-1 format
    language = models.CharField(
        max_length=2, help_text="ISO 639-1 code language format")

    # Currency is encoded in ISO 4217 format
    currency = models.CharField(
        max_length=3, help_text="ISO 4217 currency format")

    class Meta:
        ordering = ['id']


class ServiceArea(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    provider = models.ForeignKey('Provider', related_name='service_areas',
                                 on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class Coordinate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    service_area = models.ForeignKey('ServiceArea', related_name='coordinates',
                                     on_delete=models.CASCADE)


"""{
    "name": "gwarinpa",
    "price": 1200,
    "coordinates": [
          [
            [
              7.366161346435548,
              9.105995213335472
            ],
            [
              7.362728118896484,
              9.096164195829797
            ],
            [
              7.372856140136718,
              9.084298815049877
            ],
            [
              7.392253875732421,
              9.08463783138418
            ],
            [
              7.412166595458984,
              9.08701093674273
            ],
            [
              7.4288177490234375,
              9.116503933068012
            ],
            [
              7.376632690429687,
              9.121249705138204
            ],
            [
              7.366161346435548,
              9.105995213335472
            ]
          ]
        ]
}

{
            "name": "wuse",
            "price": 1900,
            "coordinates": [
                [
                    [
                        7.46315002441406,
                        9.0787049992361
                    ],
                    [
                        7.45937347412109,
                        9.07421293244803
                    ],
                    [
                        7.46057510375976,
                        9.06963605183216
                    ],
                    [
                        7.46289253234863,
                        9.06387248952033
                    ],
                    [
                        7.46829986572266,
                        9.06455056047635
                    ],
                    [
                        7.4747371673584,
                        9.06641524900385
                    ],
                    [
                        7.47525215148926,
                        9.07226352747096
                    ],
                    [
                        7.47096061706543,
                        9.07811171062109
                    ],
                    [
                        7.46315002441406,
                        9.0787049992361
                    ]
                ]
            ]
        }

{
    "name": "jahi",
    "price": 800,
    "coordinates": [
        [
            [
                7.42426872253418,
                9.10158823890483
            ],
            [
                7.42349624633789,
                9.0887060023742
            ],
            [
                7.43671417236328,
                9.08862124928315
            ],
            [
                7.44555473327637,
                9.09006204910349
            ],
            [
                7.44821548461914,
                9.09811347077598
            ],
            [
                7.45250701904297,
                9.10463922698838
            ],
            [
                7.44770050048828,
                9.1137920349901
            ],
            [
                7.43834495544434,
                9.11514798660337
            ],
            [
                7.42770195007324,
                9.11226658327188
            ],
            [
                7.42426872253418,
                9.10158823890483
            ]
        ]
    ]
}

{
    "name": "dawaki",
    "price": 500,
    "coordinates": [
          [
            [
              7.420663833618163,
              9.130063114377593
            ],
            [
              7.411479949951172,
              9.124385269918985
            ],
            [
              7.417402267456055,
              9.12133445049458
            ],
            [
              7.42049217224121,
              9.118876826990057
            ],
            [
              7.433624267578125,
              9.118622589109973
            ],
            [
              7.446928024291991,
              9.119978522377895
            ],
            [
              7.449331283569336,
              9.122181902951297
            ],
            [
              7.446155548095703,
              9.127520807139737
            ],
            [
              7.442893981933593,
              9.133283344186061
            ],
            [
              7.427959442138672,
              9.133622314052385
            ],
            [
              7.420663833618163,
              9.130063114377593
            ]
          ]
        ]
}

"""
