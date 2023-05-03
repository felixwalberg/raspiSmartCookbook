CREATE TABLE recipesNew_data (
	id int(10) NOT NULL AUTO_INCREMENT,
	Category varchar(20) NOT NULL,
	Name varchar(100) NOT NULL,
	Ingredients varchar(8000),
	Instructions varchar(8000),
	cookTemp int,
	prepTime int,
	cookTime int NOT NULL,
	totalTime int,
	servings int NOT NULL,
	PRIMARY KEY(id)
);
