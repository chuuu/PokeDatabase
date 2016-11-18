1)  cd2925


2)  http://13.68.219.167:8111/


3)  All parts of allowed user interactions specified in part 1.1 are implemented, including:
Enter a uid and retrieve a list of Pokemons owned by that user;
Enter a uid and retrieve that user’s general information;
Enter a Pokemon name and retrieve that Pokemon’s family;
Enter a PokemonFamily name and retrieve a list of Pokemons that belong to that family;
Enter a Region name and see a list of all players in that region;
Enter a Team name and see a list of all players in that team;
Store a new user’s information into the database;
Add a new Pokemon to the database; and
Modify an existing Pokemon's information.

Additionally, we implemented the following functionalities:
Display all information stored in a given table (Bag, Item, Player, Pokemon, PokemonFamily, Region and Team);
Add a new entry to any given table (Bag, Item, Player, Pokemon, PokemonFamily and Region).


4)  Since we have a single-page web front-end with several parts, we'll describe two parts of the web page that have the most interesting database operations.

Part i)  The part of the web page titled by "I want to add a new...".  This part is used to add in a new entry to any database table.  Depending on the type of the new entry user wants to add in, the webpage dynamically displays a form into which user can enter all information related to that entry, which are sent to the python server with a request, and used in a query that is sent to the actual database to add the new entry in.  The interesting thing about this part is, we implemented other queries that are run automatically if this new entry is successfully added to the database, in order to keep consistency between tables, as we initially intended.  These queries differ depending on the type of the new entry user tries to add in.  For example, if a new player is successfully added, a bag with its bid matching the new player's uid is automatically created and linked to the new player, and the total numbers of players of the region and team that player belongs to are also updated automatically.  Also, if a new item is successfully added to the database, the bag that contains the new item will automatically update its total number of items it contains to keep track of the change.

Part ii) The part of the webpage titled by "Ask Pokedata in this way!".  User enter information needed according to the directions on the webpage, such as user id, Pokemon name and so on, and these input are used in the where-clause of the query that is sent to the database to request information the user asks about.  This part is interesting because, when searching for "Pokemon family this Pokemon belongs to" and "all Pokemons in Pokemon Family", we used keyword "DISTINCT" when implementing the corresponding queries.  This is because we have a separate entry for every Pokemon rather than one entry for a type, in order to keep track of every Pokemon's ownership and level and so on.  By using "DISTINCT" we avoid having multiple entries of the same type of Pokemon, making the output on the webpage intuitively easy to read and understood by a normal user. 