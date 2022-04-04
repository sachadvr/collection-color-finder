import os
import PIL.Image

import webcolors
import valuesn

class c_color_finding:
	def __init__(self):
		self.convert()
		self.check_images()
		self.liste_pour_matteo = dict()
		vals = valuesn.c_values()

		print(str(len(self.images)) +" images were changed > Starting the program")
		print()
		for image_unique in self.images:
			print("Preparation of " + image_unique)
			dictionnaire_de_couleurs_unique = {}
			
			for item in vals.liste_de_couleurs:
				dictionnaire_de_couleurs_unique[item] = 0

			for pixelcolor in self.find_colors(image_unique):
				dictionnaire_de_couleurs_unique[self.get_colour_name(pixelcolor)[1]] += 1
			
			total = 0
			for key, value in dictionnaire_de_couleurs_unique.items(): # get total number of pixels
				total += value
			
			dictionnairefinal = dict()
			for key, value in dictionnaire_de_couleurs_unique.items(): # create a new dictionary without the colors with 0 pixels
				if value != 0:
					dictionnairefinal[key] = value

			dictionnairefinal = dict(sorted(dictionnairefinal.items(), key=lambda x: x[1], reverse=True))
			key, value = list(dictionnairefinal.items())[0] # get the first key and value

			value = (value/total) * 100 
			print("[" + image_unique + "] "+ key + " > " + str(value) + "%") 

			if key not in self.liste_pour_matteo:
				self.liste_pour_matteo[key] = 1
			else:
				self.liste_pour_matteo[key] += 1
		
		print()
		
		print("The colors most used by the brand are :")
		for key, value in self.liste_pour_matteo.items():
			if value == max(self.liste_pour_matteo.values()):
				print("[1st] "+key + " is the main color (appeared " + str(value) + "times)")
			else:
				print(key + " has appeared " + str(value) + "times")
		

	def closest_colour(self, requested_colour): 
		"""
		get the closest color to the requested color
		"""
		min_colours = {}
		for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
				r_c, g_c, b_c = webcolors.hex_to_rgb(key)
				rd = (r_c - requested_colour[0]) ** 2
				gd = (g_c - requested_colour[1]) ** 2
				bd = (b_c - requested_colour[2]) ** 2
				min_colours[(rd + gd + bd)] = name
		return min_colours[min(min_colours.keys())]

	def get_colour_name(self, requested_colour):
		"""
		get the colour name in english of the closest color
		"""
		try:
				closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
		except ValueError:
				closest_name = self.closest_colour(requested_colour)
				actual_name = None
		return actual_name, closest_name

	def check_images(self):
		"""
		get images stored in ./images and add them to the list of images
		"""
		images = []	
		for filename in os.listdir('./images'):
			if filename.endswith('.jpg') or filename.endswith('.jpeg'): 
				try:
						PIL.Image.open('./images/' + filename)
				except Exception as e:
						print(filename, 'is not a valid image')
				else:
						images.append(filename)
		self.images = images




	def find_colors(self, image):
		"""
		get the pixels colors of the image
		"""
		colors = {}
		image = PIL.Image.open('./images/' + image)
		for pixel in image.getdata():
			if pixel not in colors:
					colors[pixel] = 1
			else:
					colors[pixel] += 1
		return colors

	def convert(self):
		"""
		get images stored in ./images:notconverted and convert them to jpeg & reduce quality
		"""

		choice = input("Wanna convert images ? (y/n)")
		if choice == "n":
				return
		for filename in os.listdir('./images:notconverted'):
			if filename.endswith('.jpg') or filename.endswith('.jpeg'): 
				try:
						image = PIL.Image.open('./images:notconverted/' + filename)
						if(image.size[0] or image.size[1]) > 200:
							image.thumbnail((200, 200))
						image.save('./images/' + filename, "JPEG")
				except Exception as e:
						print(filename, 'is not a valid image')
				else:
						print("Image " + filename + " converted")