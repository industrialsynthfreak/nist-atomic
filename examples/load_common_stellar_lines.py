"""An example how program may be arranged. This loads characteristic spectral
lines for most of the stellar spectral types.
"""

from nist_atomic.loader import Loader

# Carbon stars, K and M types and brown dwarfs also have molecular lines
# such as TiO and VO.
elements_of_stellar_spectra = {
    'O': {'h', 'he ii', 'si iv', 'o iii', 'n iii', 'c iii', 'he'},
    'B': {'h', 'c ii', 'si iii', 'si iv', 'si ii', 'mg ii', 'he i'},
    'A': {'h', 'fe ii', 'mg ii', 'si ii', 'ca ii'},
    'F': {'h', 'ca ii', 'fe i', 'cr i'},
    'G': {'h', 'ca ii'},
    'K': {'mn i', 'fe i', 'si i', 'ca i', 'ni i', 'sc i', 'ba i', 'na i',
          'ca ii'},
    'M': {'h', 'fe i', 'na i', 'ca i', 'ti i', 'mg i', 'cr i'},
    'BA': {'h', 'fe i', 'na i', 'ca i', 'ti i', 'mg i', 'cr i', 'ba ii'},
    'WN': {'h', 'n iii', 'n iv', 'n v', 'he i', 'he ii'},
    'WN/C': {'n iii', 'n iv', 'he i', 'he ii', 'c iv'},
    'WC': {'c ii', 'c iii', 'c iv', 'he ii', 'he i', 'o v'},
    'WO': {'o vi', },
    'DA': {'h', },
    'DB': {'he i', },
    'DC': {},
    'DO': {'he ii', 'h', 'he i'},
}


if __name__ == '__main__':
    spectra = set.union(*list(elements_of_stellar_spectra.values()))
    Loader.load(spectra, ignore_bad_response=True)
