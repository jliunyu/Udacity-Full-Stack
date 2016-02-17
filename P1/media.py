import webbrowser


class Movie():
	'''
	the class include a constructor and three instance variables named 
	title, poster_image_url, trailer_youtube_url
	'''

	def __init__(self, movie_title, poster_image, trailer_youtube):
		'''
		initial the instance variables title using the parameter movie_title
		initial the instance variables poster_image_url using the parameter poster_image
		initial the instance variables trailer_youtube_url using the parameter trailer_youtube
		'''
		self.title = movie_title
		self.poster_image_url = poster_image
		self.trailer_youtube_url = trailer_youtube

