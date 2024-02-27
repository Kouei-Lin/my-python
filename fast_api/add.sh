#!/bin/sh

# Add movie function
add_movie() {
    curl -X POST -H "Content-Type: application/json" -d '{"title": "'"$1"'", "release_date": "'"$2"'", "score": '"$3"', "comment": "'"$4"'"}' http://localhost:8000/movies/
}

# Add ten movies
add_movie "The Shawshank Redemption" "1994-09-22" 9.3 "A classic"
add_movie "The Godfather" "1972-03-24" 9.2 "An epic crime film"
add_movie "The Dark Knight" "2008-07-18" 9.0 "A superhero film"
add_movie "Schindler's List" "1993-12-15" 8.9 "A historical drama"
add_movie "Pulp Fiction" "1994-10-14" 8.9 "A crime film"
add_movie "The Lord of the Rings: The Return of the King" "2003-12-17" 8.9 "An epic fantasy film"
add_movie "Forrest Gump" "1994-07-06" 8.8 "A comedy-drama film"
add_movie "Inception" "2010-07-16" 8.8 "A science fiction film"
add_movie "The Matrix" "1999-03-31" 8.7 "A cyberpunk action film"
add_movie "Fight Club" "1999-10-15" 8.8 "A psychological thriller film"
