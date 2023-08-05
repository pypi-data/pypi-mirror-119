"""Define a foss compatability license_matrix.

Standard disclaimer:: I am not a lawyer and there is no guarantee that the
information provided here is complete or correct. Do not take this as legal
advice on foss license compatability

https://en.wikipedia.org/wiki/IANAL


Types of license/ compatability

Public Domain
- Unlicense

Permissive Compatible
Permissive license compatible with gpl
- Mit
- Boost
- Bsd
- Isc
- Ncsa

Permissive Not Compatible
Permissive license NOT compatible with gpl
- Apache
- Eclipse
- Academic Free


Copyleft
permissive -> lgpl 2.1 -> gpl 2
permissive -> lgpl 3 -> gpl 3 -> agpl
permissive -> mpl -> gpl -> agpl (3 only)

permissive (any) -> EU
EU -> gpl -> agpl (3 only)
"""
from __future__ import annotations

from licensecheck.types import License


def licenseType(lice: str) -> list[License]:
	"""Return a list of license types from a license string.

	Args:
		lice (str): license name

	Returns:
		list[License]: the license
	"""
	licenses = []
	liceL = lice.split(", ")  # Deal with multilicense
	for liceS in liceL:
		lice = liceS.upper()
		if "PUBLIC DOMAIN" in lice:
			licenses.append(License.PUBLIC)
		elif "UNLICENSE" in lice:
			licenses.append(License.UNLICENSE)

		elif "MIT" in lice:
			licenses.append(License.MIT)
		elif "BOOST" in lice:
			licenses.append(License.BOOST)
		elif "BSD" in lice:
			licenses.append(License.BSD)
		elif "ISC" in lice:
			licenses.append(License.ISC)
		elif "NCSA" in lice:
			licenses.append(License.NCSA)
		elif "PYTHON" in lice:
			licenses.append(License.PSFL)

		elif "APACHE" in lice:
			licenses.append(License.APACHE)
		elif "ECLIPSE" in lice:
			licenses.append(License.ECLIPSE)
		elif "AFL" in lice:
			licenses.append(License.ACADEMIC_FREE)

		elif "LGPL" in lice:
			if "LGPLV2+" in lice:
				licenses.append(License.LGPL_2_PLUS)
			elif "LGPLV3+" in lice:
				licenses.append(License.LGPL_3_PLUS)
			elif "LGPLV2+" in lice:
				licenses.append(License.LGPL_2_PLUS)
			elif "LGPLV3+" in lice:
				licenses.append(License.LGPL_3_PLUS)
			else:
				licenses.append(License.LGPL_X)
		elif "AGPL" in lice:
			licenses.append(License.AGPL_3_PLUS)
		elif "GPL" in lice:
			if "GPLV2+" in lice:
				licenses.append(License.GPL_2_PLUS)
			elif "GPLV3+" in lice:
				licenses.append(License.GPL_3_PLUS)
			elif "GPLV2+" in lice:
				licenses.append(License.GPL_2_PLUS)
			elif "GPLV3+" in lice:
				licenses.append(License.GPL_3_PLUS)
			else:
				licenses.append(License.GPL_X)

		elif "MPL" in lice:
			licenses.append(License.MPL)
		elif "EUPL" in lice:
			licenses.append(License.EU)
		else:
			licenses.append(License.NO_LICENSE)
	return licenses


# Permissive licenses compatible with GPL
PERMISSIVE = [
	License.MIT,
	License.BOOST,
	License.BSD,
	License.ISC,
	License.NCSA,
	License.PSFL,
]
# Permissive licenses NOT compatible with GPL
PERMISSIVE_OTHER = [
	License.APACHE,
	License.ECLIPSE,
	License.ACADEMIC_FREE,
]
# LGPL licenses
LGPL = [
	License.LGPL_2,
	License.LGPL_3,
	License.LGPL_2_PLUS,
	License.LGPL_3_PLUS,
	License.LGPL_X,
]
# GPL licenses (including AGPL)
GPL = [
	License.GPL_2,
	License.GPL_3,
	License.GPL_2_PLUS,
	License.GPL_3_PLUS,
	License.GPL_X,
	License.AGPL_3_PLUS,
]
# Other Copyleft licenses
OTHER_COPYLEFT = [
	License.MPL,
	License.EU,
]

# Basic compat matrix
UNLICENSE_INCOMPATIBLE = (
	PERMISSIVE + PERMISSIVE_OTHER + GPL + LGPL + OTHER_COPYLEFT + [License.NO_LICENSE]
)
PERMISSIVE_INCOMPATIBLE = GPL + [License.EU, License.NO_LICENSE]
LGPL_INCOMPATIBLE = GPL + OTHER_COPYLEFT + PERMISSIVE_OTHER + [License.NO_LICENSE]
GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [License.AGPL_3_PLUS, License.NO_LICENSE]
PERMISSIVE_GPL_INCOMPATIBLE = PERMISSIVE_OTHER + [License.NO_LICENSE]

# GPL compat matrix
# https://www.gnu.org/licenses/gpl-faq.html#AllCompatibility
GPL_2_INCOMPATIBLE = [License.GPL_3, License.GPL_3_PLUS, License.LGPL_3, License.LGPL_3_PLUS]
L_GPL_3_INCOMPATIBLE = [License.GPL_2]


def depCompatWMyLice(
	myLicense: License,
	depLice: list[License],
	ignoreLicenses: list[License] = None,
	failLicenses: list[License] = None,
) -> bool:
	"""Identify if the end user license is compatible with the dependency license(s).

	Args:
		myLicense (License): end user license to check
		depLice (list[License]): dependency license
		ignoreLicenses (list[License], optional): list of licenses to ignore. Defaults to None.
		failLicenses (list[License], optional): list of licenses to fail on. Defaults to None.

	Returns:
		bool: True if compatible, otherwise False
	"""
	blacklist = {
		License.UNLICENSE: UNLICENSE_INCOMPATIBLE,
		License.PUBLIC: UNLICENSE_INCOMPATIBLE,
		License.MIT: PERMISSIVE_INCOMPATIBLE,
		License.BOOST: PERMISSIVE_INCOMPATIBLE,
		License.BSD: PERMISSIVE_INCOMPATIBLE,
		License.ISC: PERMISSIVE_INCOMPATIBLE,
		License.NCSA: PERMISSIVE_INCOMPATIBLE,
		License.PSFL: PERMISSIVE_INCOMPATIBLE,
		License.APACHE: PERMISSIVE_INCOMPATIBLE,
		License.ECLIPSE: PERMISSIVE_INCOMPATIBLE,
		License.ACADEMIC_FREE: PERMISSIVE_INCOMPATIBLE,
		License.LGPL_X: LGPL_INCOMPATIBLE,
		License.LGPL_2: LGPL_INCOMPATIBLE,
		License.LGPL_3: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.LGPL_2_PLUS: LGPL_INCOMPATIBLE,
		License.LGPL_3_PLUS: LGPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.GPL_X: GPL_INCOMPATIBLE,
		License.GPL_2: GPL_INCOMPATIBLE + GPL_2_INCOMPATIBLE,
		License.GPL_3: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.GPL_2_PLUS: GPL_INCOMPATIBLE,
		License.GPL_3_PLUS: GPL_INCOMPATIBLE + L_GPL_3_INCOMPATIBLE,
		License.AGPL_3_PLUS: PERMISSIVE_GPL_INCOMPATIBLE,
		License.MPL: LGPL + GPL + [License.EU],
		License.EU: PERMISSIVE_GPL_INCOMPATIBLE + LGPL + GPL + [License.MPL],
	}
	# Protect against None
	failLicenses = failLicenses or []
	ignoreLicenses = ignoreLicenses or []
	blacklistResolved = blacklist[myLicense]
	for lice in depLice:
		if lice in failLicenses or (lice not in ignoreLicenses and lice in blacklistResolved):
			return False
	return True
