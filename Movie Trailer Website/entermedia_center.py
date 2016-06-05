import media
import fresh_tomatoes


# Create a new instance of Movie class named minions_story
minions_story = media.Movie("Minions", 
		"http://www.hercampus.com/sites/default/files/2015/06/22/Minions-2.jpg", 
		"https://www.youtube.com/watch?v=lC4i6FYFoSc")

# Create a new instance of Movie class named gumball_story
gumball_story = media.Movie("Gumball", 
		"http://i.jeded.com/i/the-amazing-world-of-gumball-third-season.29094.jpg", 
		"https://www.youtube.com/watch?v=6lxXVDwBpyg")

# Create a new instance of Movie class named jurassicWorld_store
jurassicWorld_store = media.Movie("Jurassic World", 
		"http://images-cdn.moviepilot.com/images/c_fill,h_1051,w_1600/t_mp_quality/vmqmrneddreefpnb3ct8/the-best-fan-made-posters-for-jurassic-world-386131.jpg", 
		"https://www.youtube.com/watch?v=gB7Fm2NmWF8")

# Create a new instance of Movie class named captainAmerica_store
captainAmerica_store = media.Movie("Captain America", 
		"http://s3.amazonaws.com/images.hitfix.com/assets/883/CaptainAmericaExclusivePoster.jpg", 
		"https://www.youtube.com/watch?v=R9xgkBlrEn0")

# Create a new instance of Movie class named theAvengers_store
theAvengers_store = media.Movie("The Avengers", 
		"http://img2.wikia.nocookie.net/__cb20120506232435/disney/images/4/45/The_Avengers_poster.jpg", 
		"https://www.youtube.com/watch?v=W9ZnpIGvZUo")

# Create a new instance of Movie class named spiderMan_store
spiderMan_store = media.Movie("Spider-Man", 
		"http://fc00.deviantart.net/fs71/f/2014/055/f/c/the_amazing_spider_man_2_post	er_fanmade_by_augustohag-d77u05w.jpg", 
		"https://www.youtube.com/watch?v=w4Hwfkfn0N8")

# store all the instance to a list
movies = [minions_story, gumball_story, jurassicWorld_store, captainAmerica_store, theAvengers_store, spiderMan_store]

# call the open_movies_page function from the fresh_tomatoes
fresh_tomatoes.open_movies_page(movies)