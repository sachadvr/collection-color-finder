import webcolors

class c_values:
	def __init__(self):
		liste_de_couleurs = []
		for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
			liste_de_couleurs.append(name)
		self.liste_de_couleurs = liste_de_couleurs